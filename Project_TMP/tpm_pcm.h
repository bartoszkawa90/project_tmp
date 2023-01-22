#ifndef TPM_PCM_H
#define TPM_PCM_H
#include "frdm_bsp.h"


void TPM0_Init_PCM(void);

void TPM0_PCM_Play(void);//uint8_t song);
extern uint8_t signal[];
extern uint8_t speed;
extern int32_t timer;
extern uint32_t TIME;
extern uint8_t play_index;
extern uint8_t playFlag;
extern const uint16_t SAMPLES;

#endif /* TPM_PCM_H */
