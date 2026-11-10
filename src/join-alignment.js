/** One correction for a midpoint load that YouTube restarts at zero.
 * No periodic drift seeking, ad detection, control interception or ad skipping.
 */
export class JoinAlignment {
  load(videoId,offset){this.pending={videoId,offset};}
  stop(){this.pending=null;}
  playing({videoId,time,duration,expectedDuration,elapsed},seek){
    const pending=this.pending;
    if(!pending||videoId!==pending.videoId||![time,duration,expectedDuration,elapsed].every(Number.isFinite)||expectedDuration<=0||Math.abs(duration-expectedDuration)>Math.max(5,expectedDuration*.01))return false;
    this.pending=null; // The first coherent content-playing sample consumes this load.
    if(pending.offset<10||time>=5||elapsed<15||elapsed-time<=10||elapsed>=duration-1)return false;
    try{seek(elapsed);return true;}catch{return false;}
  }
}
