export type Slide={id:string;name:string;width:number;height:number;status:string;pyramid_levels:number};
export type Region={id:number;x:number;y:number;width:number;height:number;score:number};
export type Annotation={id:number;type:'POINT'|'RECTANGLE'|'NOTE';x:number;y:number;width:number;height:number;text:string};
export type ScannerEvent={type:string;job_id:string;payload:{x?:number;y?:number;progress?:number;retries?:number;error?:string}};
