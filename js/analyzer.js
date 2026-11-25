'use strict';
// Offline analyzer. Input is normalized mono PCM; no device access.
function analyze(samples, rate) {
  if (!samples || samples.length < 32 || samples.length > 8192 || !Number.isFinite(rate) || rate < 8000 || rate > 192000) throw new Error('Invalid PCM frame');
  const n=samples.length;
  let sum=0, peak=0;
  for(const x of samples){if(!Number.isFinite(x)||Math.abs(x)>1)throw new Error('PCM must be normalized');sum+=x*x;peak=Math.max(peak,Math.abs(x));}
  const bands={bass:0,mid:0,treble:0};
  let dominantHz=0, max=0;
  for(let k=1;k<=Math.floor(n/2);k++){
    const hz=k*rate/n;
    if(hz<20||hz>20000)continue;
    let re=0,im=0;
    for(let j=0;j<n;j++){
      const x=samples[j]*(0.5-0.5*Math.cos(2*Math.PI*j/(n-1)));
      const a=2*Math.PI*k*j/n;
      re+=x*Math.cos(a);im-=x*Math.sin(a);
    }
    const p=(re*re+im*im)/(n*n);
    bands[hz<250?'bass':hz<2000?'mid':'treble']+=p;
    if(p>max){max=p;dominantHz=hz;}
  }
  const total=bands.bass+bands.mid+bands.treble;
  for(const key of Object.keys(bands))bands[key]=total>0?bands[key]/total:0;
  return {rms:Math.sqrt(sum/n),peak,dominantHz,bands};
}
module.exports={analyze};
