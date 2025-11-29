#ifndef _fsm_fsm_h
#define _fsm_fsm_h

#include "state.h"

class CFSM
{
	protected:
		CState* m_pCurrentState;
		CState* m_pNewState;
		CStateTemplate<CFSM> m_stateInitial;

	public:
		CFSM();
		virtual ~CFSM() {}

		virtual void Update();

		bool IsState(CState &State) const;
		bool GotoState(CState &NewState);

		virtual void BeginStateInitial() {}
		virtual void StateInitial() {}
		virtual void EndStateInitial() {}
};

#endif
