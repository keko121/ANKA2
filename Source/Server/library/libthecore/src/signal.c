/*
 *    Filename: signal.c
 * Description: Signal handling functions
 *
 *      Author: Cronan
 */

#define __LIBTHECORE__

#ifdef __WIN32__

#include "stdafx.h"

void signal_setup() {}
void signal_timer_disable() {}
void signal_timer_enable(int timeout_seconds) {}

#else
// Unix (Linux, FreeBSD)

// Signal constants for Linux x86_64
#define MY_SIGHUP    1
#define MY_SIGINT    2
#define MY_SIGALRM   14
#define MY_SIGTERM   15
#define MY_SIGCHLD   17
#define MY_SIGUSR1   10
#define MY_SIGPIPE   13
#define MY_SIGVTALRM 26

// Signal function types
typedef void (*sighandler_t)(int);
#define MY_SIG_IGN ((sighandler_t)1)

// Declare signal function from libc
extern "C" sighandler_t signal(int signum, sighandler_t handler);

// System headers
extern "C" {
#include <sys/wait.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdlib.h>
}

#include "stdafx.h"

static void reap(int sig)
{
    while (waitpid(-1, NULL, WNOHANG) > 0);
    signal(MY_SIGCHLD, reap);
}

static void checkpointing(int sig)
{
    if (!tics)
    {
        sys_err("CHECKPOINT shutdown: tics did not updated.");
        abort();
    }
    else
        tics = 0;
}

static void hupsig(int sig)
{
    shutdowned = TRUE;
    sys_err("SIGHUP, SIGINT, SIGTERM signal has been received. shutting down.");
}

static void usrsig(int sig)
{
    core_dump();
}

void signal_timer_disable(void)
{
    struct itimerval itime;
    struct timeval interval;

    interval.tv_sec = 0;
    interval.tv_usec = 0;

    itime.it_interval = interval;
    itime.it_value = interval;

    setitimer(ITIMER_VIRTUAL, &itime, NULL);
}

void signal_timer_enable(int sec)
{
    struct itimerval itime;
    struct timeval interval;

    interval.tv_sec = sec;
    interval.tv_usec = 0;

    itime.it_interval = interval;
    itime.it_value = interval;

    setitimer(ITIMER_VIRTUAL, &itime, NULL);
}

void signal_setup(void)
{
    signal_timer_enable(30);

    signal(MY_SIGVTALRM, checkpointing);

    signal(MY_SIGHUP, hupsig);
    signal(MY_SIGCHLD, reap);
    signal(MY_SIGINT, hupsig);
    signal(MY_SIGTERM, hupsig);
    signal(MY_SIGPIPE, MY_SIG_IGN);
    signal(MY_SIGALRM, MY_SIG_IGN);
    signal(MY_SIGUSR1, usrsig);
}

#endif
