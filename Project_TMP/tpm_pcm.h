/******************************************************************************
 * This file is a part of the SM2 Tutorial (C).                               *                                                 *
 ******************************************************************************/

/**
 * @file tpm_pcm.h
 * @author Koryciak
 * @date Nov 2020
 * @brief File containing enums, structures and declarations for TPM.
 * @ver 0.1
 */

#ifndef TPM_PCM_H
#define TPM_PCM_H
#include "frdm_bsp.h"


/**
 * @brief TPM0 initialization. PCM.
 */
void TPM0_Init_PCM(void);
/**
 * @brief Play wave once.
 *
 */
void TPM0_PCM_Play(uint8_t song);
extern uint8_t signal[];
extern uint8_t speed;
extern int32_t timer;
extern uint32_t TIME;
extern uint8_t play_index;
extern uint8_t playFlag;
extern const uint16_t SAMPLES;

#endif /* TPM_PCM_H */
