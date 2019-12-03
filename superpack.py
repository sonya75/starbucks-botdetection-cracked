import struct
from collections import OrderedDict
class TypeTags:
    UINT6_BASE=0
    UINT14_BASE=64
    NINT4_BASE=128
    BARRAY4_BASE=144
    ARRAY5_BASE=160
    STR5_BASE=192
    FALSE=224
    TRUE=225
    NULL=226
    UNDEFINED=227
    UINT16=228
    UINT24=229
    UINT32=230
    UINT64=231
    NINT8=232
    NINT16=233
    NINT32=234
    NINT64=235
    FLOAT32=236
    DOUBLE64=237
    TIMESTAMP=238
    BINARY_=239
    CSTRING=240
    STR8=241
    STR_=242
    STRREF=243
    ARRAY8=244
    ARRAY_=245
    BARRAY8=246
    BARRAY_=247
    MAP_=248
    BMAP_=249
    MAPL_=250
    BMAPL_=251
    STRLUT=254
    EXTENSION=255
def bytefrombools(x):
	y=[]
	for i in range(0,len(x),8):
		a,j=0,0
		while j<8 and j<(len(x)-i):
			a|=int(x[i+j])<<(7-j)
			j+=1
		y.append(a)
	return y
def int32tobytes(x):
	return [x>>24,x>>16&0xFF,x>>8&0xFF,x&0xFF]
class Encoder:
	def __init__(self):
		self.keysets=[]
		self.keysetsindex=0
		self.stringhist={}
		self.output=[]
	def createstringhist(self,obj):
		if type(obj)==str or type(obj)==unicode:
			obj=obj.encode('utf-8')
			self.stringhist[obj]=self.stringhist.get(obj,0)+1
			return
		if type(obj)==list:
			for p in obj:
				self.createstringhist(p)
		elif type(obj)==dict:
			for p in obj:
				self.createstringhist(obj[p])
	def encode(self,obj,keysetstoomit=None):
		if keysetstoomit==None: keysetstoomit=[]
		self.keysets=[tuple(p) for p in keysetstoomit]
		self.keysetsindex=len(self.keysets)
		self.output=[]
		self.stringhist=OrderedDict()
		self.createstringhist(obj)
		self.stringhist=[(p,((len(p) + 1) * self.stringhist[p]) - (len(p) + 2 + self.stringhist[p])) for p in self.stringhist]
		self.stringhist=[(-q,p) for (p,q) in self.stringhist if q>0]
		self.stringhist=[p for (q,p) in sorted(self.stringhist)]
#		self.stringhist=['password','INPUT','username','BUTTON','probably','23127127','03130','Google Inc.','LABEL','HTML' ]
		q=self.stringhist
		if len(self.stringhist)>255:
			self.stringhist=self.stringhist[:255]
		self.write(obj)
		x=self.output
		self.output=[]
		self.stringhist=[]
		self.output.append(TypeTags.STRLUT)
		self.output.append(len(q))
		for p in q:
			self.writeStr(p)
		self.writeArray(self.keysets[self.keysetsindex:])
		return self.output+x

	def write(self,x):
		if type(x)==type(None):
			self.output.append(TypeTags.NULL)
		elif x==NULL:
			self.output.append(TypeTags.NULL)
		elif x==UNDEFINED:
			self.output.append(TypeTags.UNDEFINED)
		elif x==INFINITY:
			self.output+=[TypeTags.FLOAT32,0x7F,0x80,0x00,0x00]
		elif x==NEGINFINITY:
			self.output+=[TypeTags.FLOAT32,0xFF,0x80,0x00,0x00]
		elif x==NAN:
			self.output+=[TypeTags.FLOAT32,0x7F,0xC0,0x00,0x00]
		else:
			ENCODERS[type(x)](self,x)
	def writeBoolean(self,x):
		if x: self.output.append(TypeTags.TRUE)
		else: self.output.append(TypeTags.FALSE)
	def writeInt(self,x):
		if abs(x)>0xFFFFFFFFFFFFFFFF:
			return self.writeFloat(x)
		if x>=0:
			if x<64:
				self.output.append(x)
			elif x<=0x3FFF:
				self.output+=[TypeTags.UINT14_BASE|x>>8,x&0xFF]
			elif x<=0xFFFF:
				self.output+=[TypeTags.UINT16,x>>8,x&0xFF]
			elif x<=0xFFFFFF:
				self.output+=[TypeTags.UINT24,x>>16,x>>8&0xFF,x&0xFF]
			elif x<=0xFFFFFFFF:
				self.output.append(TypeTags.UINT32)
				self.output+=int32tobytes(x)
			else:
				self.output.append(TypeTags.UINT64)
				self.output+=int32tobytes(x>>32&0xFFFFFFFF)
				self.output+=int32tobytes(x&0xFFFFFFFF)
		else:
			x=-x
			if x<=15:
				self.output.push(TypeTags.NINT4_BASE|x)
			elif x<=0xFF:
				self.output+=[TypeTags.NINT8,x]
			elif x<=0xFFFF:
				self.output+=[TypeTags.NINT16,x>>8,x&0xFF]
			elif x<=0xFFFFFFFF:
				self.output.append(TypeTags.NINT32)
				self.output+=int32tobytes(x)
			else:
				self.output.append(TypeTags.NINT64)
				self.output+=int32tobytes(x>>32&0xFFFFFFFF)
				self.output+=int32tobytes(x&0xFFFFFFFF)
	def writeFloat(self,x):
		m=struct.pack("f",x)
		if x==struct.unpack("f",m)[0]:
			self.output.append(TypeTags.FLOAT32)
		else:
			self.output.append(TypeTags.DOUBLE64)
			m=struct.pack("d",x)
		self.output+=[ord(m[i]) for i in range(len(m)-1,-1,-1)]
	def writeStr(self,x):
		x=x.encode('utf-8')
		if x in self.stringhist:
			self.output+=[TypeTags.STRREF,self.stringhist.index(x)]
			return
		z=False
		xe=[]
		for p in x:
			p=ord(p)
			if p==0:
				z=True
			xe.append(p)
		x=xe
		y=len(x)
		if y<32:
			self.output.append(TypeTags.STR5_BASE|y)
			self.output+=x
		else:
			if not z:
				self.output.append(TypeTags.CSTRING)
				self.output+=x
				self.output.append(0)
			else:
				if y<=255:
					self.output+=[TypeTags.STR8,y]
				else:
					self.output.append(TypeTags.STR_)
					self.writeInt(y)
				self.output+=x

	def writeArray(self,x):
		isboolarray=True
		for p in x:
			if type(x)!=bool:
				isboolarray=False
				break
		if isboolarray:
			if len(x)<16:
				self.output.append(TypeTags.BARRAY4_BASE|len(x))
			elif len(x)<256:
				self.output.append(TypeTags.BARRAY8)
				self.output.append(len(x))
			else:
				self.output.append(TypeTags.BARRAY_)
				self.writeInt(len(x))
			self.output+=bytefrombools(x)
		else:
			if len(x)<32:
				self.output.append(TypeTags.ARRAY5_BASE|len(x))
			elif len(x)<=255:
				self.output.append(TypeTags.ARRAY8)
				self.output.append(len(x))
			else:
				self.output.append(TypeTags.ARRAY_)
				self.writeInt(len(x))
			for p in x:
				self.write(p)
	def writeDict(self,x):
		y=tuple(sorted(x.keys()))
		try:
			k=self.keysets.index(y)
		except:
			self.keysets.append(y)
			k=len(self.keysets)-1
		isbool=True
		for p in y:
			if type(x[p])!=bool:
				isbool=False
				break
		if isbool:
			self.output.append(TypeTags.BMAP_)
			self.writeInt(k)
			self.output+=bytefrombools([x[p] for p in y])
		else:
			self.output.append(TypeTags.MAP_)
			self.writeInt(k)
			for p in y:
				self.write(x[p])
ENCODERS={
	list:Encoder.writeArray,
	dict:Encoder.writeDict,
	str:Encoder.writeStr,
	unicode:Encoder.writeStr,
	bool:Encoder.writeBoolean,
	float:Encoder.writeFloat,
	long:Encoder.writeInt,
	int:Encoder.writeInt,
	tuple:Encoder.writeArray
}
class NULL: pass
class UNDEFINED: pass
class NAN: pass
class INFINITY: pass
class NEGINFINITY: pass

__all__=['NULL','UNDEFINED','NAN','INFINITY','NEGINFINITY','Encoder']

def test():
	import json
	x=json.loads(open("superpacktest",'rb').read())
	x=Encoder().encode(x,[["timestamp"],["channelCount","channelCountMod","channelInterpretation","fftSize","frequencyBinCount","maxChannelCount","maxDecibels","minDecibels","numberOfInputs","numberOfOutputs","sampleRate","smoothingTimeConstant","state"],["hash","max","min"],["audio/mpeg","audio/ogg","audio/wav","audio/wave","audio/webm"],["hasDefaultBrowserHelper","hasWidevinePlugin","plugins"],["dataFragment","hashcode"],["hasToSource","sourceHash","stringHash"],["computedStyleHash"],["background-repeat: round space;","border-image: none;","border-radius: 4px;","color: var(companyblue);","display: run-in;","filter: blur(2px);","flow-into: main-thread;","grid-columns: auto 1fr;","hyphens: auto;","inline-block: none;","mask-repeat: repeat-x;","mask: auto;","object-fit: contain;","overflow-scrolling: touch;","position: sticky;","resize: both;","tab-size: 4;","text-stroke: 2.0px;","user-select: none;","word-break: auto;"],["","-moz-","-ms-","-webkit-"],["-moz-osx-font-smoothing","-webkit-app-region","-webkit-text-size-adjust","animation","column-count","hyphens","justify-items","text-align-last","text-emphasis","text-orientation"],["caughtException","userAgentStyleHash"],[],["global"],["pageXOffset","pageYOffset"],["fonts","version"],["callable","documentElement","exists","falsy","nullish","type"],["foreignElements","links"],["innerText","tagName","xpath"],["d83d-dc69-d83c-dffb-200d-2764-fe0f-200d-d83d-dc69-d83c-dffe","d83d-dd2b","d83d-ddfe","d83d-decd","d83e-dd16","d83e-dd8b"],["alpha","colors"],["avg","count","volume"],["b","g","r"],["emptyReferrer","historyLength"],["completeness","id","seen"],["keyDown","keyPress","keyUp"],["altKey","ctrlKey","eventType","instanceOfUIEvent","keyCode","markedAsTrusted","metaKey","sequenceNumber","shiftKey","target","timestamp"],["eventType","keyCode","modifierKeys","sequenceNumber","target","timestamp"],["language","languages"],["hash","mathProperties"],["mouseClick","mouseDown","mouseMove","mouseUp"],["button","eventType","instanceOfUIEvent","markedAsTrusted","oX","oY","sequenceNumber","target","timestamp","x","y"],["button","eventType","instanceOfUIEvent","markedAsTrusted","target","timestamp","x","y"],["mouseButtonEvents","mouseMoveEvents"],["button","eventType","sequenceNumber","target","timestamp","x","y"],["recent","throttled"],["eventType","timestamp","x","y"],["argumentsValue","hasArguments","hasGlobal","hasProcess"],["nonce"],["avgAlpha","avgBeta","avgGamma","avgInterval","numOrientationEvents","stdDevAlpha","stdDevBeta","stdDevGamma","stdDevInterval"],["connectStart","domComplete","domContentLoadedEventEnd","domContentLoadedEventStart","domInteractive","domLoading","loadEventEnd","loadEventStart","requestStart","responseEnd","responseStart"],["statuscode","value"],["document","documentBody","external","global","navigator"],["ActiveXObject","ApplePaySession","File","Int8Array","MutationObserver","Notification","PushManager","SharedWorker","TouchEvent","XDomainRequest","_Selenium_IDE_Recorder","__fxdriver_unwrapped","_phantom","addEventListener","attachEvent","awesomium","callPhantom","createPopup","detachEvent","dispatchEvent","domAutomationController","event","external","fireEvent","frames","getComputedStyle","globalStorage","localStorage","mozRTCPeerConnection","mozRequestAnimationFrame","phantom","postMessage","registerProtocolHandler","removeEventListener","requestAnimationFrame","sessionStorage","sidebar","webkitRTCPeerConnection","webkitRequestAnimationFrame","webkitResolveLocalFileSystemURL"],["$cdc_asdjflasutopfhvcZLmcfl_","_Selenium_IDE_Recorder","__fxdriver_unwrapped","__webdriver_script_fn","all","characterSet","charset","compatMode","documentMode","getElementById","getElementsByClassName","hasAttributes","images","layers","querySelector"],["contextMenu","innerHTML","innerText","mozRequestFullScreen","requestFullScreen","webdriver","webkitRequestFullScreen"],["vibrate"],["Sequentum"],["crypto","document","documentBody","external","global","navigator"],["ActiveXObject","ApplePaySession","BluetoothUUID","File","MutationObserver","Notification","PushManager","SharedWorker","TouchEvent","XDomainRequest","_Selenium_IDE_Recorder","__fxdriver_unwrapped","_phantom","attachEvent","callPhantom","createPopup","detachEvent","event","external","fireEvent","frameElement","globalStorage","localStorage","mozRTCPeerConnection","mozRequestAnimationFrame","netscape","phantom","postMessage","registerProtocolHandler","requestAnimationFrame","sessionStorage","sidebar","webkitRTCPeerConnection","webkitRequestAnimationFrame","webkitResolveLocalFileSystemURL"],["$cdc_asdjflasutopfhvcZLmcfl_","_Selenium_IDE_Recorder","__fxdriver_unwrapped","__webdriver_script_fn","all","characterSet","charset","compatMode","documentMode","images","layers"],["contextMenu","innerText","mozRequestFullScreen","requestFullScreen","webkitRequestFullScreen"],["bluetooth","credentials","requestMediaKeySystemAccess","storage","vibrate","webdriver"],["subtle"],["global","locationbar","navigator","operaVersion","screen","toolbar"],["devicePixelRatio","innerHeight","innerWidth","isSecureContext","outerHeight","outerWidth","screenX","screenY"],["availHeight","availWidth","colorDepth","height","pixelDepth","width"],["appCodeName","appName","appVersion","buildID","cpuClass","doNotTrack","hardwareConcurrency","maxTouchPoints","oscpu","platform","product","productSub","userAgent","vendor","vendorSub","webdriver"],["ip","model"],["constructor","lastChance"],["events"],["accuracy","timestamp","x","y","z"],["level","powerSource","status","technology","temp","voltage"],["androidId","board","deviceBrand","deviceModel","deviceModelNumber","hardware","hardwareName","manufacturer","osBuildFingerprint","osBuildNumber","osName","osVersion","product","serial"],["availableRam","availableStorage","totalRam","totalStorage"],["bignox","bluestacks","genymotion","superuser"],["kernelPatch"],["country","currency","language","timezone"],["accuracy","distance","timestamp"],["density","height","width"],["configId","errorArray","kernelId","kernelURI","kernelUpdateHeaderName","lastErrorCount","lastErrorId","lastErrorTimestamp","timeSinceLastRequest"],["jvmVersion","osArch","osName","osVersion"],["timestamp","x","y","z"],["level","status"],["appBundleName","appInstallId","appVersion","cfBundleInfo","deviceBrand","deviceModel","deviceModelNumber","intAppVersion","osType","osVersion","sdkVersion"],["availableStorage","numCores","timestamp","totalRam","uptimeSinceBoot"],["brightness","density","height","width"],["hw.cputype","hw.model","hw.physicalcpu","kern.boottime","kern.hostname","kern.proc","kern.version"],["appdir"],["jailbreak"],["data","mnt","storage"],["eth0","p2p0","wlan0"],["root"],["cpuinfo","date","uname","whoami"],["net.hostname","ro.boot.boottime","ro.build.date.utc","ro.build.fingerprint","ro.runtime.firstboot","serialno"],["afterReady","immediately","lastChance"],["InstallTrigger","controllers"],["status","value"],["bodyAttribute","scriptPresent"],["hash"],["description","message","name","num","stack","stacktrace"],["length","punctuators","whitespace"],["touchEnd","touchMove","touchStart"],["eventType","timestamp","touches"],["oX","oY","x","y"],["x","y"],["3gpp; codecs=\"mp4v.20.8, samr\"","mp2t; codecs=\"avc1.42E01E,mp4a.40.2\"","mp4","mp4; codecs=\"avc1.42c00d\"","mp4; codecs=\"avc1.64001E, mp4a.40.2\"","mp4; codecs=\"mp4v.20.8, mp4a.40.2\"","mp4; codecs=bogus","mp4; codecs=mp4a.40.2","mpeg","ogg; codecs=\"theora, speex\"","ogg; codecs=opus","ogg; codecs=speex","ogg; codecs=theora","wav; codecs=\"0\"","wav; codecs=\"1\"","wav; codecs=\"2\"","wave","wave; codecs=0","wave; codecs=1","wave; codecs=2","webm; codecs=\"vorbis,vp9\"","webm; codecs=\"vp8, vorbis\"","webm; codecs=vorbis","x-mpeg","x-mpegurl"],["events","finalState","initialState","visibilityEventCount"],["timestamp","visible"],["contextProperties","parameters","shaderPrecisions","supportedExtensions"],["antialias","debugInfo","dimensions","maxAnisotropy","params"],["alphaBits","blueBits","depthBits","greenBits","maxCombinedTextureImageUnits","maxCubeMapTextureSize","maxFragmentUniformVectors","maxRenderbufferSize","maxTextureImageUnits","maxTextureSize","maxVaryingVectors","maxVertexAttribs","maxVertexTextureImageUnits","maxVertexUniformVectors","redBits","renderer","shadingLanguageVersion","stencilBits","vendor","version"],["renderer","vendor"],["candidate","ip"],["hasSpeechSynthesis","voiceData"],["hash","match","noOfDefaultVoices","noOfVoices","relLang","relVoiceUri"],["bursts","events"],["errors","signals"]])
	print x
	print len(x)