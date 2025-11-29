#pragma once

#ifdef ENABLE_BIOLOG_SYSTEM
#include "utils.h"
#include <functional>
#include <map>
#include <memory>

struct SArgumentSupportImpl
{
	void * Ptr_to_data;

	void * GetPointerToData()
	{
		return Ptr_to_data;
	}

	virtual ~SArgumentSupportImpl() {}
};

class CEventFunctionHandler : public singleton<CEventFunctionHandler>
{
	struct SFunctionHandler
	{
		std::function<void(SArgumentSupportImpl *)> func;
		size_t time;
		size_t baseTime;
		std::unique_ptr<SArgumentSupportImpl> SupportArg;
		bool bPersisting;
		
		SFunctionHandler(std::function<void(SArgumentSupportImpl *)> _func, const size_t & _time, SArgumentSupportImpl * support_arg = nullptr, bool bPersisting_ = false)
		{
			func = _func;
			baseTime = _time;
			time = _time+get_global_time();
			SupportArg = std::unique_ptr<SArgumentSupportImpl>(support_arg);
			bPersisting = bPersisting_;
		}
		
		void UpdateTime(const size_t & newtime)
		{
			time = newtime+get_global_time();
		}

		bool IsPersisting()
		{
			return bPersisting;
		}

		time_t GetBaseTime()
		{
			return baseTime;
		}
	};

	public:
		CEventFunctionHandler();
		virtual ~CEventFunctionHandler();
		void Destroy();

	public:
		void CreateEvent(DWORD dwEventPtr, std::function<void(SArgumentSupportImpl *)> func, const std::string & event_name, const size_t & runtime, SArgumentSupportImpl * support_arg, bool bPersisting);
		void CancelEvent(DWORD dwEventPtr, const std::string & event_name);
		bool AddEvent(std::function<void(SArgumentSupportImpl *)> func, const std::string & event_name, const size_t & runtime, SArgumentSupportImpl * support_arg = nullptr, bool bPersisting = false);
		void RemoveEvent(const std::string & event_name);
		void DelayEvent(const std::string & event_name, const size_t & newtime);
		bool FindEvent(const std::string & event_name);
		DWORD GetDelay(const std::string & event_name);
		void Process();

	private:
		SFunctionHandler * GetHandlerByName(const std::string & event_name);
		std::map<std::string, std::unique_ptr<SFunctionHandler> > m_event;
		bool bProcessStatus;
};
#endif
