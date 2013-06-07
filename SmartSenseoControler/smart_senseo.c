//*****************************************************************************
//
// smart_senseo.c - This program is for enableing Senseo coffe maker for
// wireless control over bluetooth.
//
// University of applied science Kiel
// This work is done by the students:
// Marco Neumann 915215
// Nils Bürkner 915205
// Ambient Intelligence / Prof. Dr. Manzke
//
// This Software is based on the uart_echo example from TI. We used the source
// code to get into uart communication with the launchpad.
//
// This project was done while the ami lecture and is a part of intellignet
// home. The other side of this coffe maker the application for communicate
// with this software can be a bluetooth 2.0 enabled smart phone. Our idea in
// that case is that you can program an alarm clock that makes you a coffe
// while wakeing you up. If you would press snooze because you are lazy the app
// would wait with makeing a coffe until you are ready to get up and you decline
// the snooze function.
//
//*****************************************************************************

#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "inc/lm4f120h5qr.h"
#include "driverlib/debug.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "driverlib/uart.h"
#include <string.h>


volatile char rfid[10]={0,0,0,0,0,0,0,0,0,0};
volatile char rfid1[10]={0,0,0,0,0,0,0,0,0,0};
volatile char rfid2[10]={0,0,0,0,0,0,0,0,0,0};
volatile char status[5]={0,0,0,0,0};
volatile char command=0xff;
volatile char led=0x00;
volatile char equal;

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void __error__(char *pcFilename, unsigned long ulLine){
}
#endif

//*****************************************************************************
//
// The UART interrupt handler for the serial debug (usb) connection.
// For integration you have to change a bit code in Startup.s file. there you 
// have to add a line over the vector table with the sentence 
// EXTERN  UARTIntHandler and you have to add the name UARTIntHandler in the
// vector table instead of IntDefaultHandler at the position ; UART0 Rx and Tx.
//
//*****************************************************************************
void UART0_usb_IntHandler(void){
    unsigned long ulStatus;
		long value;
	  //
    // Get the interrrupt status.
    //
    ulStatus = UARTIntStatus(UART0_BASE, true);
    //
    // Clear the asserted interrupts.
    //
    UARTIntClear(UART0_BASE, ulStatus);
    //
    // Loop while there are characters in the receive FIFO.
    //
    while(UARTCharsAvail(UART0_BASE))
    {		
				value=UARTCharGet(UART0_BASE);
				UARTCharPut(UART0_BASE, value);			
    }
}

//*****************************************************************************
//
// The UART interrupt handler for the bluetooth connection.
//
//*****************************************************************************
void UART1_bt_IntHandler(void){
    unsigned long ulStatus;
		//
    // Get the interrrupt status.
    //
    ulStatus = UARTIntStatus(UART1_BASE, true);
    //
    // Clear the asserted interrupts.
    //
    UARTIntClear(UART1_BASE, ulStatus);
    //
    // Loop while there are characters in the receive FIFO.
    //
	  while(UARTCharsAvail(UART1_BASE))
    {
				command=UARTCharGet(UART1_BASE)&0x0f;
				UARTCharPut(UART0_BASE, command);			
    }
}

//*****************************************************************************
//
// The UART interrupt handler for the rfid connection.
//
//*****************************************************************************
void UART4_rfid_IntHandler(void){
    unsigned long ulStatus;
		int i;
		//
    // Get the interrrupt status.
    //
    ulStatus = UARTIntStatus(UART4_BASE, true);
    //
    // Clear the asserted interrupts.
    //
    UARTIntClear(UART4_BASE, ulStatus);
    //
    // Loop while there are characters in the receive FIFO.
    //
		i=0;
    while(UARTCharsAvail(UART4_BASE))
    {
				rfid[i]=UARTCharGet(UART4_BASE);
				i++;
    }
}

//*****************************************************************************
//
// This function counts the external interrupts to measure the frequence of
// the LED. This is required to figure out if the Senseo is heating up, ready
// or is out of water.
//
//*****************************************************************************
void GPIO_PortD_IntHandler(void){
  GPIOPinIntClear(GPIO_PORTD_BASE, GPIO_PIN_3);
	led++;
}



//*****************************************************************************
//
// This function of our SMART_SENSEO project returns the status value.
//
//*****************************************************************************
void get_status(){
	int i;
	int counter;
	char led_tmp=0x00;

	status[0]=0x00;
	
	for (i=0; i<=9; i++)
		rfid1[i]=rfid[i];
					
	led=0;
	//
	// Delay for 2* 1000 millisecond.  Each SysCtlDelay is about 3 clocks.
	//
	SysCtlDelay(2*(SysCtlClockGet() / (1 * 3)));
	//
	// Getting the status of the led (ready, water is heating up, to few water left)
	//
	led_tmp=led;
	
					
	for (i=0; i<=9; i++)
		rfid2[i]=rfid[i];

	for (i=0; i<=9; i++){
		if (rfid1[i]==rfid2[i])
			equal=1;
		else
			equal=0;
	}
					
	if (equal == 1){
		status[1]=rfid1[1];
		status[2]=rfid1[2];
		status[3]=rfid1[3];
		status[4]=rfid1[4];
	}else{
		status[1]=0xff;
		status[2]=0xff;
		status[3]=0xff;
		status[4]=0xff;
	}
	
	counter=0;
	for(i=1;i<5;i++){
		if (status[i]>0x00 && status[i]<0xff)
			counter++;
	}
	
	
	//Set all bits of the information byte depending on existing 	
	if (counter==4)
		status[0]|=0x08;
	//detect falling edges for verifying in which frequence the led is blinking 
	if (led_tmp==0 && !GPIOPinRead(GPIO_PORTD_BASE, GPIO_PIN_3)){//machine ready
		status[0]|=0x02;
		status[0]|=0x01;
	}else if (led_tmp==0 && GPIOPinRead(GPIO_PORTD_BASE, GPIO_PIN_3)){
		status[0]&=~0x02;
		status[0]&=~0x01;
	}else if (led_tmp==1 || led==2)
		status[0]|=0x07;
	else{
		status[0]|=0x01;
		status[0]&=0x09;
	}
	
	//sends the infomation string to the user application
	for (i=0; i<5; i++){
		UARTCharPut(UART1_BASE, status[i]);
		UARTCharPut(UART0_BASE, status[i]);		
	}
	for (i=0; i<=9; i++){
		rfid1[i]=0;
		rfid2[i]=0;
		rfid[i]=0;
	}
	for (i=0; i<=5; i++)
		status[i]=0;
}


//*****************************************************************************
//
// This is the main function of our SMART_SENSEO project.
// The first part of this function is the initalization of all registers. The
// second one is........................................................................................................
//
//*****************************************************************************
int main(void){
    //
    // Enable lazy stacking for interrupt handlers.  This allows floating-point
    // instructions to be used within interrupt handlers, but at the expense of
    // extra stack usage.
    //
    FPUEnable();
    FPULazyStackingEnable();

    //
    // Set the clocking to run directly from the crystal.
    //
    SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC | SYSCTL_OSC_MAIN |
                       SYSCTL_XTAL_16MHZ);
	
		//
    // Enable processor interrupts.
    //
    IntMasterEnable();
		
    //
    // Enable the peripheral for Outputs to control the Senseo
		// 3 outputs and 1 input are required
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
		
    //
    // Enable the peripherals for UART0, UART1, UART4
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
		
		SysCtlPeripheralEnable(SYSCTL_PERIPH_UART1);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
		
		SysCtlPeripheralEnable(SYSCTL_PERIPH_UART4);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);
		
		//
    // Enable the GPIO pins for setting and reading the senseo status
		// PD0=on/off, PD1=small_cup, PD2=tall_cup
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTD_BASE, GPIO_PIN_0);
		GPIOPinTypeGPIOOutput(GPIO_PORTD_BASE, GPIO_PIN_1);
		GPIOPinTypeGPIOOutput(GPIO_PORTD_BASE, GPIO_PIN_2);
				
		//
		// Make PD3 an input
		//
		GPIOPinTypeGPIOInput(GPIO_PORTD_BASE, GPIO_PIN_3);
		
		//
		//Enable pullup for Pin PD3 (the output strength is not recognized)
		//
		GPIOPadConfigSet(GPIO_PORTD_BASE, GPIO_PIN_3, GPIO_STRENGTH_8MA, GPIO_PIN_TYPE_STD_WPU);
		
		//
		// Enable Interrupts for Pin PD3 on falling edge
		//
		GPIOIntTypeSet(GPIO_PORTD_BASE, GPIO_PIN_3,GPIO_FALLING_EDGE);
		GPIOPinIntClear(GPIO_PORTD_BASE, GPIO_PIN_3);
		GPIOPinIntEnable(GPIO_PORTD_BASE, GPIO_PIN_3);
		
		//Nasted vectored interrupt controller
		IntPrioritySet(INT_GPIOD, 0xA0);
		IntEnable(INT_GPIOD);

		//
		// Debug (usb) interface
    // Set GPIO A0 and A1 as UART pins.
		// Configure the UART for 115,200, 8-N-1 operation
		// Enable the UART interrupt
    //
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);
		
		UARTConfigSetExpClk(UART0_BASE, SysCtlClockGet(), 115200,
                            (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE |
                             UART_CONFIG_PAR_NONE));
		
		IntEnable(INT_UART0);
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);
		
		//
		// Bluetooth interface
    // Set GPIO B0 and B1 as UART pins.
		// Configure the UART for 115,200, 8-N-1 operation
		// Enable the UART interrupt
    //
		GPIOPinConfigure(GPIO_PB0_U1RX);
    GPIOPinConfigure(GPIO_PB1_U1TX);
    GPIOPinTypeUART(GPIO_PORTB_BASE, GPIO_PIN_0 | GPIO_PIN_1);
		
		UARTConfigSetExpClk(UART1_BASE, SysCtlClockGet(), 115200,
                            (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE |
                             UART_CONFIG_PAR_NONE));
		
		IntEnable(INT_UART1);
    UARTIntEnable(UART1_BASE, UART_INT_RX | UART_INT_RT);
		
		//
		// RFID interface
    // Set GPIO C4 and C5 as UART pins.
		// Configure the UART for 9600, 8-N-1 operation
		// Enable the UART interrupt
    //
		GPIOPinConfigure(GPIO_PC4_U4RX);
    GPIOPinConfigure(GPIO_PC5_U4TX);
    GPIOPinTypeUART(GPIO_PORTC_BASE, GPIO_PIN_4 | GPIO_PIN_5);
		
		UARTConfigSetExpClk(UART4_BASE, SysCtlClockGet(), 9600,
                            (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE |
                             UART_CONFIG_PAR_NONE));
		
    IntEnable(INT_UART4);
    UARTIntEnable(UART4_BASE, UART_INT_RX | UART_INT_RT);
						
		equal=0;
		//
    // Loop forever to make tasty coffe
    //
    while(1)
    {			
			if (command == 0x09){
						UARTCharPut(UART0_BASE, command);
						//
						// Set PD0 to high and switch senseo on or off
						//
						GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_0, 1);
						//
						// Delay for 100 millisecond.  Each SysCtlDelay is about 3 clocks.
						//
						SysCtlDelay(SysCtlClockGet() / (10 * 3));
						//
						// Set PD0 to low to get on off switch in idle state
						//
						GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_0, 0);
					status[0]=0x00;
					get_status();
					command=0xff;
				}else if (command == 0x0A){
					UARTCharPut(UART0_BASE, command);
					//
					// Set PD1 to high and make a small cup
					//
					GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_1, 2);
					//
					// Delay for 100 millisecond.  Each SysCtlDelay is about 3 clocks.
					//
					SysCtlDelay(SysCtlClockGet() / (10 * 3));
					//
					// Set PD1 to low to get small cup in idle state
					//
					GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_1, 0);
					status[0]=0x00;
					get_status();
					command=0xff;
				}else if (command == 0x0C){
					UARTCharPut(UART0_BASE, command);
					//
					// Set PD2 to high and make a tall cup
					//
					GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_2, 4);
					//
					// Delay for 100 millisecond.  Each SysCtlDelay is about 3 clocks.
					//
					SysCtlDelay(SysCtlClockGet() / (10 * 3));
					//
					// Set PD2 to low to get tall cup in idle state
					//
					GPIOPinWrite(GPIO_PORTD_BASE, GPIO_PIN_2, 0);
					get_status();
					command=0xff;
				}else if (command == 0x08){
					UARTCharPut(UART0_BASE, command);
					status[0]=0x00;
					get_status();
					command=0xff;
				}
    }
}

