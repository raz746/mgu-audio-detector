'use strict';
const assert=require('assert');
const {analyze}=require('./analyzer');
const rate=16000,n=1024;
for(const [hz,band] of [[125,'bass'],[1000,'mid'],[4000,'treble']]){
 const pcm=Array.from({length:n},(_,i)=>0.5*Math.sin(2*Math.PI*hz*i/rate));
 const r=analyze(pcm,rate);
 assert(Math.abs(r.dominantHz-hz)<=rate/n);
 assert(r.bands[band]>0.95);
 assert(Math.abs(r.rms-Math.sqrt(0.125))<0.01);
 console.log(hz+' Hz',JSON.stringify(r));
}
assert.strictEqual(analyze(new Array(n).fill(0),rate).rms,0);
console.log('All synthetic tests passed');
