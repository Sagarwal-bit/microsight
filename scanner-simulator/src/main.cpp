#include "scanner.hpp"
#include <cstdlib>
#include <iostream>
#include <sstream>
using namespace microsight;
static void callback(const Event& e){std::cout<<e.type<<" x="<<e.x<<" y="<<e.y<<" progress="<<e.progress<<"%\n"; const char* url=std::getenv("BACKEND_URL");if(!url)return;std::ostringstream json;json<<"{\"event_type\":\""<<e.type<<"\",\"job_id\":\""<<e.job_id<<"\",\"payload\":{\"x\":"<<e.x<<",\"y\":"<<e.y<<",\"progress\":"<<e.progress<<",\"retries\":"<<e.retries<<"}}";std::string cmd="curl -fsS --max-time 3 -H 'Content-Type: application/json' -d '"+json.str()+"' "+std::string(url)+"/api/scanner/events/ >/dev/null || echo scanner_callback_unavailable >&2";std::system(cmd.c_str());}
int main(int argc,char**argv){Failure fail=Failure::NONE;for(int i=1;i<argc;i++){std::string a=argv[i];if(a=="--help"){std::cout<<"microsight_scanner --demo [--fail-focus|--fail-camera]\n";return 0;}if(a=="--fail-focus")fail=Failure::FOCUS_FAILURE;if(a=="--fail-camera")fail=Failure::CAMERA_TIMEOUT;}Scanner scanner;bool ok=scanner.scan({"demo-job",4,4},FailureInjector(fail),callback);std::cout<<"Final state: "<<state_name(scanner.state())<<"\n";return ok?0:1;}
