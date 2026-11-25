'use strict';
// Read-only inventory; no recording, subprocesses, or vehicle controls.
const fs=require('fs');
function names(p){try{return fs.readdirSync(p).sort().slice(0,100);}catch(e){return [];}}
function read(p){try{return fs.readFileSync(p,'utf8').slice(0,12000);}catch(e){return null;}}
const report={schema:1,status:'INVENTORY_ONLY',platform:process.platform,
 audioDeviceNames:names('/dev/snd'),
 alsaCards:read('/proc/asound/cards'),
 alsaDevices:read('/proc/asound/devices'),
 configPaths:['/etc/asound.conf','/etc/pulse','/etc/pipewire'].filter(p=>fs.existsSync(p))};
console.log(JSON.stringify(report,null,2));
