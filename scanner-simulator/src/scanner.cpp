#include "scanner.hpp"
#include <chrono>
#include <thread>
using namespace std::chrono_literals;
namespace microsight {
bool StageController::move_to(int,int,Failure f){std::this_thread::sleep_for(12ms);return f!=Failure::MOTOR_TIMEOUT;}
bool FocusController::autofocus(Failure f){std::this_thread::sleep_for(8ms);return f!=Failure::FOCUS_FAILURE;}
bool CameraController::capture(Failure f){std::this_thread::sleep_for(10ms);return f!=Failure::CAMERA_TIMEOUT && f!=Failure::CORRUPTED_TILE;}
bool RetryManager::run(const std::function<bool()>& action){for(attempts_=0;attempts_<=maximum_;++attempts_){if(action())return true;if(attempts_<maximum_)std::this_thread::sleep_for(std::chrono::milliseconds(delay_ms_*(1<<attempts_)));}return false;}
Scanner::Scanner(int retries):retries_(retries){} ScannerState Scanner::state()const{std::lock_guard<std::mutex> lock(mutex_);return state_;} void Scanner::set(ScannerState s){std::lock_guard<std::mutex> lock(mutex_);state_=s;} void Scanner::connect(){set(ScannerState::IDLE);}
bool Scanner::scan(ScanJob job,FailureInjector injector,const std::function<void(const Event&)>& emit){connect();emit({"SCAN_STARTED",job.id});for(int y=0;y<job.rows;y++)for(int x=0;x<job.columns;x++){Failure f=injector.for_tile(x,y);set(ScannerState::MOVING);if(!stage_.move_to(x,y,f)){set(ScannerState::FAILED);emit({"SCAN_FAILED",job.id,x,y});return false;}set(ScannerState::FOCUSING);if(!focus_.autofocus(f)){set(ScannerState::FAILED);emit({"SCAN_FAILED",job.id,x,y});return false;}set(ScannerState::CAPTURING);RetryManager retry(retries_);if(!retry.run([&]{return camera_.capture(f);})){set(ScannerState::FAILED);emit({"TILE_FAILED",job.id,x,y,retry.attempts()});return false;}set(ScannerState::IDLE);job.progress=100.0*(y*job.columns+x+1)/(job.columns*job.rows);emit({"TILE_SAVED",job.id,x,y,retry.attempts(),job.progress});}set(ScannerState::COMPLETED);emit({"SCAN_COMPLETED",job.id,job.columns-1,job.rows-1,0,100});return true;}
std::string state_name(ScannerState s){static const char* n[]={"DISCONNECTED","IDLE","MOVING","FOCUSING","CAPTURING","ERROR","COMPLETED","FAILED"};return n[(int)s];} std::string failure_name(Failure f){static const char* n[]={"NONE","CAMERA_TIMEOUT","FOCUS_FAILURE","MOTOR_TIMEOUT","NETWORK_FAILURE","CORRUPTED_TILE"};return n[(int)f];}
}
