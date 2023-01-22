#include "MKL05Z4.h"
#include "uart0.h"
#include "led.h"
#include "tpm_pcm.h"
//#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "tsi.h"


// IMPORTANT
#define LF	0xa
#define READ  0x1
#define COMMAND  0xcc
#define CHECK_CON  0xc

char read = 0;
char com = 0;
char command[16];
uint16_t rx_sig_pos=0;
uint8_t rx_com_pos=0;
char temp;
uint8_t rx_FULL=0;
uint8_t too_long=0;
uint8_t  check = 0;
char PLAY[] = ">";
char GOBACK[] = "!";
char STOP[] = "|";
char CLEAR_ALL[] = "!!!";

// ADDITIONAL
uint16_t frequencies[] = {350, 401, 452, 502, 553, 604, 654, 704};
// czestotliwosci do wyswitlania w Hz
char Error[]="Zla komenda";
char Checked[] = "Connection works";
char Too_Long[]="Zbyt dlugi ciag";


void clear_command(){
	for(uint8_t c; c<16; c++){
		command[c] = 0;
	}
}

void UART0_IRQHandler()
{
	if(UART0->S1 & UART0_S1_RDRF_MASK)
	{
		temp=UART0->D;	// Odczyt wartosci z bufora odbiornika i skasowanie flagi RDRF
		if ( check == 0 && temp == CHECK_CON ) check = 1;
		if ( temp == READ && read == 0 ) read = 1;
		else if ( temp == COMMAND && com == 0) com = 1;
		else 
		{
			// Read signal
			if (read==1 && com==0) 
			{
				if(!rx_FULL)
				{
					if(temp!=LF)
					{
						if(!too_long)	// Jesli za dlugi ciag, ignoruj reszte znak�w
						{
							signal[rx_sig_pos] = temp;	// Kompletuj komende
							rx_sig_pos++;
							if(rx_sig_pos==SAMPLES){
								too_long=1;		// Za dlugi ciag
							}
						} 
					}
					else
					{
						if(!too_long)	signal[rx_sig_pos] = 0;  // Jesli za dlugi ciag, porzuc tablice 
						rx_FULL=1;
						read = 0;
					}
				}
			}
			// Read comand
			if (read==1 && com==1) 
			{
				if(!rx_FULL)
				{
					if(temp!=LF)
					{
						if(!too_long)	// Jesli za dlugi ciag, ignoruj reszte znak�w
						{
							command[rx_com_pos] = temp;	// Kompletuj komende
							rx_com_pos++;
							if(rx_com_pos==16)
								too_long=1;		// Za dlugi ciag
						}
					}
					else
					{
						if(!too_long)	command[rx_com_pos] = 0;  // Jesli za dlugi ciag, porzuc tablice 
						rx_FULL=1;
						read = 0;
						com = 0;
					}
				}
			}
		}
		NVIC_EnableIRQ(UART0_IRQn);
	}
}

//uint8_t* data;


int main(void)
{	
	//data = malloc(16000);
	char a[] = {(char)speed};
	uint8_t i, current_slider;
	uint8_t slider = 0;
	LED_Init();
	LCD1602_Init();		 // Inicjalizacja wyswietlacza 
	LCD1602_Backlight(TRUE);
	LCD1602_SetCursor(0,1);
	UART0_Init();		// Inicjalizacja  UART0
	//LCD1602_Print("Send song ...");
	TPM0_Init_PCM ();
	TSI_Init ();
	
	while(1)	
	{
		LCD1602_SetCursor(0,0);
		sprintf(a,"Frequency = %2d",frequencies[signal[play_index]]);		
		LCD1602_Print(a);
		LCD1602_SetCursor(0,1);
		sprintf(a,"Signal  =  %2d",signal[20]);		
		LCD1602_Print(a);
		
		
		// SLIDER 
		current_slider = TSI_ReadSlider();
		
		if ( current_slider != slider){
			slider = current_slider;
			play_index = slider;
		}
		
		/*if ( slider > 0 & slider < 40 ){
			TPM0_PCM_Play(1);
		}
		else if (slider > 56 & slider < 100){
			TPM0_PCM_Play(0);
			playFlag = 0;
		}*/
		
		
		//  SENDING RESPONSE
		if ( check == 1){
			for(i=0;Checked[i]!=0;i++)	// Zla komenda
			{
				while(!(UART0->S1 & UART0_S1_TDRE_MASK));	// Czy nadajnik gotowy?
				  UART0->D = Checked[i];
				}
				while(!(UART0->S1 & UART0_S1_TDRE_MASK));	// Czy nadajnik gotowy?
					UART0->D = 0xa;		// Nastepna linia
		}
		check = 0;
		
			
		if(rx_FULL)		// Czy dana gotowa?
		{
			if(too_long)
			{
				for(i=0;Too_Long[i]!=0;i++)	// Zbyt dlugi ciag
					{
						while(!(UART0->S1 & UART0_S1_TDRE_MASK));	// Czy nadajnik gotowy?
						UART0->D = Too_Long[i];
					}
					while(!(UART0->S1 & UART0_S1_TDRE_MASK));	// Czy nadajnik gotowy?
					UART0->D = 0xa;		// Nastepna linia
					too_long=0;
			}
			else
			{
				if(strcmp (command,PLAY)==0){ 
						LCD1602_SetCursor(0,1);
						LCD1602_Print("Playing ...     ");
						TPM0_PCM_Play(1); 
				}
				else if (strcmp (command,GOBACK)==0){
						LCD1602_SetCursor(0,1);
						LCD1602_Print("Back to start   ");
						speed = 34;
						timer = 0;
						play_index = 0;
						playFlag = 0;
				}
				else if (strcmp (command,STOP)==0){
						TPM0_PCM_Play(0);
						LCD1602_SetCursor(0,1);
						LCD1602_Print("Stopped         ");
						playFlag = 0;
				}
				else if (strcmp (command,CLEAR_ALL)==0){
						for ( i=0;i<SAMPLES;i++){
								signal[i] = 0;
						}
						LCD1602_SetCursor(0,1);
						LCD1602_Print("Data Cleared    ");
						speed = 34;
						timer = 0;
						play_index = 0;
						playFlag = 0;
						clear_command();
				}
				else
				{
						for(i=0;Error[i]!=0;i++)	// Zla komenda
						{
							while(!(UART0->S1 & UART0_S1_TDRE_MASK));	// Czy nadajnik gotowy?
							UART0->D = Error[i];
						}
						while(!(UART0->S1 & UART0_S1_TDRE_MASK));	// Czy nadajnik gotowy?
						UART0->D = 0xa;		// Nastepna linia
					}
				}
			rx_com_pos = 0;
			rx_sig_pos = 0;
			rx_FULL=0;	// Dana skonsumowana
		}
		/*if ( signal[0] != 0 && command[0] != 0){
			LCD1602_SetCursor(0,2);
			LCD1602_Print("Com & Sig  ");
		}
		else if( signal[0] == 0 && command[0] != 0){
			LCD1602_SetCursor(0,2);
			LCD1602_Print("Only Com  ");
		}
		else {
			LCD1602_SetCursor(0,2);
			LCD1602_Print("Only Sig  ");
		}*/
	}
}