/* Compatibility shims for the Chrome 69 production target; not a TV certification. */
(function(g){
  if(typeof g.globalThis==='undefined')g.globalThis=g;
  if(!Array.prototype.at)Object.defineProperty(Array.prototype,'at',{configurable:true,writable:true,value:function(index){var n=Math.trunc(Number(index)||0);if(n<0)n=this.length+n;return n<0||n>=this.length?undefined:this[n];}});
  if(g.Element&&!Element.prototype.replaceChildren)Element.prototype.replaceChildren=function(){while(this.firstChild)this.removeChild(this.firstChild);for(var i=0;i<arguments.length;i++){var child=arguments[i];this.appendChild(child&&child.nodeType?child:document.createTextNode(String(child)));}};
  if(!Promise.allSettled)Promise.allSettled=function(values){return Promise.all(Array.from(values).map(function(value){return Promise.resolve(value).then(function(result){return {status:'fulfilled',value:result};},function(reason){return {status:'rejected',reason:reason};});}));};
})(typeof window!=='undefined'?window:this);
