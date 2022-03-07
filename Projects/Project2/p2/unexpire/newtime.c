#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <dlfcn.h>

// Name: Craig Li
// netID: craigli
// RUID: 133000399
// your code for time() goes here

//hardcoded time for Feb 1, 2021
time_t fake_time = (long int) 1612155600;
static int initFlag = 0;

time_t time(time_t *tloc){

    time_t (*original_time)(time_t *tloc);
    original_time = dlsym(RTLD_NEXT, "time");

    //we only need to give a fake time once
    if(initFlag == 0){
        initFlag = 1;
        *tloc = fake_time;
        return fake_time;
    }
    //after this, just pass the current time
    //set tloc if it isn't NULL
    time_t curr = (time_t) original_time(tloc);
    if(tloc != NULL){
        *tloc = curr;
    }
    return curr;
}