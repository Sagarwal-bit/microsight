#pragma once
#include <atomic>
#include <functional>
#include <mutex>
#include <string>

namespace microsight {
enum class ScannerState { DISCONNECTED, IDLE, MOVING, FOCUSING, CAPTURING, ERROR, COMPLETED, FAILED };
enum class Failure { NONE, CAMERA_TIMEOUT, FOCUS_FAILURE, MOTOR_TIMEOUT, NETWORK_FAILURE, CORRUPTED_TILE };
struct Event { std::string type, job_id; int x=0, y=0, retries=0; double progress=0; };
struct ScanJob { std::string id; int columns=4, rows=4; int current_x=0, current_y=0; double progress=0; };
class StageController { public: bool move_to(int, int, Failure); };
class FocusController { public: bool autofocus(Failure); };
class CameraController { public: bool capture(Failure); };
class RetryManager { public: explicit RetryManager(int maximum=2, int delay_ms=25): maximum_(maximum),delay_ms_(delay_ms){} bool run(const std::function<bool()>&); int attempts() const { return attempts_; } private:int maximum_,delay_ms_,attempts_=0; };
class FailureInjector { public: explicit FailureInjector(Failure f=Failure::NONE):failure_(f){} Failure for_tile(int x,int y) const { return x==1&&y==1?failure_:Failure::NONE; } private:Failure failure_; };
class Scanner { public: explicit Scanner(int retries=2); ScannerState state() const; void connect(); bool scan(ScanJob, FailureInjector, const std::function<void(const Event&)>&); private: void set(ScannerState); mutable std::mutex mutex_; ScannerState state_=ScannerState::DISCONNECTED; StageController stage_; FocusController focus_; CameraController camera_; int retries_; };
std::string state_name(ScannerState); std::string failure_name(Failure);
}
