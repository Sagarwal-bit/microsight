#include "scanner.hpp"
#include <cassert>
using namespace microsight;
int main(){Scanner s;assert(s.state()==ScannerState::DISCONNECTED);s.connect();assert(s.state()==ScannerState::IDLE);int events=0;assert(s.scan({"test",2,2},FailureInjector{},[&](const Event&){events++;}));assert(s.state()==ScannerState::COMPLETED);assert(events==6);Scanner failed;assert(!failed.scan({"fail",2,2},FailureInjector(Failure::CAMERA_TIMEOUT),[](const Event&){}));assert(failed.state()==ScannerState::FAILED);RetryManager retry(2,0);assert(retry.run([]{return true;}));return 0;}
