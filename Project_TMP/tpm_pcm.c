#include "tpm_pcm.h"
#include "wave1.h"

#define UPSAMPLING 1
void TPM0_IRQHandler(void);
//static uint8_t tpm0Enabled = 0;

static uint16_t upSampleCNT = 0;
static uint16_t sampleCNT = 0;
uint8_t  playFlag = 0;    //  troche zbedna

const uint16_t  SAMPLES = 200;
uint8_t speed = 1;
uint32_t TIME_END = 1309360;//163670;
uint32_t timer = 0;
uint8_t play_index = 0;

uint8_t what_to_play = 0;
uint8_t signal[SAMPLES];
//char signal[CONTROL_SAMPLES] = {0,8, 1,8, 2,8, 3,8, 4,8, 5,8, 6,8, 7,8};


void TPM0_Init_PCM(void) {
			
  SIM->SCGC6 |= SIM_SCGC6_TPM0_MASK;		
	SIM->SOPT2 |= SIM_SOPT2_TPMSRC(1);    // CLK ~ 41,9MHz (CLOCK_SETUP=0)

	SIM->SCGC5 |= SIM_SCGC5_PORTB_MASK; 
	PORTB->PCR[7] = PORT_PCR_MUX(2);			// PCM output -> PTB7, TPM0 channel 2
	
	TPM0->SC |= TPM_SC_PS(0);  					  // 41,9MHz          // 4 ~ 10,48MHz
	TPM0->SC |= TPM_SC_CMOD(1);					  // internal input clock source

	TPM0->MOD = 255; 										  // 8bit PCM
																				//  41,9 MHz / 256 = 163,67 kHz                             //10,48MHz / 256 ~ 40,96kHz
	
// "Edge-aligned PWM true pulses" mode -> PCM output
	TPM0->SC &= ~TPM_SC_CPWMS_MASK; 		
	TPM0->CONTROLS[2].CnSC |= (TPM_CnSC_MSB_MASK | TPM_CnSC_ELSB_MASK); 
	TPM0->CONTROLS[2].CnV = 0; 
	
	
// "Output compare" -> for intterrupt
	TPM0->SC &= ~TPM_SC_CPWMS_MASK;
	TPM0->CONTROLS[0].CnSC |= (TPM_CnSC_MSA_MASK | TPM_CnSC_ELSA_MASK);
	TPM0->CONTROLS[0].CnV = 0;
  
	TPM0->CONTROLS[0].CnSC |= TPM_CnSC_CHIE_MASK; // Enable interrupt
	
	NVIC_SetPriority(TPM0_IRQn, 1);  // TPM0 interrupt priority level 

	NVIC_ClearPendingIRQ(TPM0_IRQn); 
	NVIC_EnableIRQ(TPM0_IRQn);	// Enable Interrupts 
	
	//tpm0Enabled = 1;  // set local flag 
}

void TPM0_PCM_Play(uint8_t song) {
	sampleCNT = 0;   // start from the beginning 
	playFlag = 1;    //  troche zbedna
	speed = signal[play_index];
	what_to_play = song;
}

void TPM0_IRQHandler(void) {
	if (playFlag) {
		if ( what_to_play == 1){
		
			if (upSampleCNT == 0) {
				sampleCNT = sampleCNT+speed; // +4 leci 4 razy szybciej   4 x f
				TPM0->CONTROLS[2].CnV = SIN[sampleCNT]; // load new sample
			}
			if (sampleCNT > sizeof(SIN)){ //WAVE1_SAMPLES) {
				//playFlag = 0;         // stop if at the end
				//TPM0->CONTROLS[2].CnV = 0;
				sampleCNT = 0;
			}
			// 40,96kHz / 10 ~ 4,1kHz ~ WAVE_RATE
			if (++upSampleCNT > (UPSAMPLING-1)) upSampleCNT = 0;
		}
		
		
	/*
	else if (what_to_play == 2 ){
		if (playFlag) {
			if (upSampleCNT == 0) TPM0->CONTROLS[2].CnV = signal[sampleCNT++]; // load new sample
			if (sampleCNT > sizeof(signal)){ //WAVE1_SAMPLES) {
				playFlag = 0;         // stop if at the end
				TPM0->CONTROLS[2].CnV = 0;
			}
			// 40,96kHz / 10 ~ 4,1kHz ~ WAVE_RATE
			if (++upSampleCNT > (UPSAMPLING-1)) upSampleCNT = 0;
		}
	}*/
	
	
		if ( signal[play_index] == 0){
			play_index += 2;
		}
		else {
			speed = frequency[signal[play_index]-1];
			timer += signal[play_index+1];
			if ( timer >= TIME_END ){
				timer = 0;
				if ( play_index == SAMPLES-2) play_index = 0;
				else play_index += 2;
				if ( play_index >= SAMPLES) {
					play_index = 0;
				}
			}
		}
	}
	TPM0->CONTROLS[0].CnSC |= TPM_CnSC_CHF_MASK; 
}



