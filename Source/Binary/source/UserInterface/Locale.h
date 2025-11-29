#pragma once

#include "StdAfx.h"

unsigned GetCodePage();
int StringCompareCI (LPCSTR szStringLeft, LPCSTR szStringRight, size_t sizeLength);
void LoadConfig(const char *fileName);
unsigned GetGuildLastExp(int level);
int GetSkillPower(unsigned level);

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
BYTE LocaleService_GetLocaleID();
bool LocaleService_SaveLocale(int iCodePage, const char *szLocale);
const char *LocaleService_GetLocale();
#endif

const char *LocaleService_GetLocaleName();
const char *LocaleService_GetLocalePath();