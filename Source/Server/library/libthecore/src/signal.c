/*
 *    Filename: signal.c
 * Description: Signal handling functions
 *
 *      Author: Cronan
 */

// _GNU_SOURCE must be defined before any includes for signal constants
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

// For C++ compilation, use csignal
#ifdef __cplusplus
#include <csignal>
#include <cstdlib>
using std::signal;
#else
#include <signal.h>
#include <stdlib.h>
#endif

#include <sys/wait.h>
#include <sys/time.h>
#include <unistd.h>

// Define signal constants if not defined (Linux C++ compatibility)
#ifndef SIGCHLD
#define SIGCHLD 17
#endif
#ifndef SIGHUP
#define SIGHUP 1
#endif
#ifndef SIGINT
#define SIGINT 2
#endif
#ifndef SIGTERM
#define SIGTERM 15
#endif
#ifndef SIGPIPE
#define SIGPIPE 13
#endif
#ifndef SIGALRM
#define SIGALRM 14
#endif
#ifndef SIGUSR1
#define SIGUSR1 10
#endif
#ifndef SIGVTALRM
#define SIGVTALRM 26
#endif
#ifndef SIG_IGN
#define SIG_IGN ((void(*)(int))1)
#endif

#define __LIBTHECORE__
#include "stdafx.h"

#ifdef __WIN32__
void signal_setup() {}
void signal_timer_disable() {}
void signal_timer_enable(int timeout_seconds) {}
#elif defined(__FreeBSD__) || defined(__linux__)
#define RETSIGTYPE void

RETSIGTYPE reap(int sig)
{
    while (waitpid(-1, NULL, WNOHANG) > 0);
    signal(SIGCHLD, reap);
}


RETSIGTYPE checkpointing(int sig)
{
    if (!tics)
    {
	sys_err("CHECKPOINT shutdown: tics did not updated.");
	abort();
    }
    else
	tics = 0;
}


RETSIGTYPE hupsig(int sig)
{
    shutdowned = TRUE;
    sys_err("SIGHUP, SIGINT, SIGTERM signal has been received. shutting down.");
}

RETSIGTYPE usrsig(int sig)
{
    core_dump();
}

void signal_timer_disable(void)
{
    struct itimerval itime;
    struct timeval interval;

    interval.tv_sec	= 0;
    interval.tv_usec	= 0;

    itime.it_interval = interval;
    itime.it_value = interval;

    setitimer(ITIMER_VIRTUAL, &itime, NULL);
}

void signal_timer_enable(int sec)
{
    struct itimerval itime;
    struct timeval interval;

    interval.tv_sec	= sec;
    interval.tv_usec	= 0;

    itime.it_interval = interval;
    itime.it_value = interval;

    setitimer(ITIMER_VIRTUAL, &itime, NULL);
}

void signal_setup(void)
{
    signal_timer_enable(30);

    signal(SIGVTALRM, checkpointing);

    /* just to be on the safe side: */
    signal(SIGHUP, hupsig);
    signal(SIGCHLD, reap);
    signal(SIGINT, hupsig);
    signal(SIGTERM, hupsig);
    signal(SIGPIPE, SIG_IGN);
    signal(SIGALRM, SIG_IGN);
    signal(SIGUSR1, usrsig);
}

#endif
