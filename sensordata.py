import time,random,os,re,base64,json,struct
from shape_encrypt import encrypt
from superpack import *
def simplehash(x):
    if type(x)!=list:
        xx=[]
        i=-2
        for i in range(0,len(x)-1,2):
            xx.append(ord(x[i])<<16|ord(x[i+1]))
        if i<(len(x)-2):
            xx.append(ord(x[-1])<<16)
        x=xx
    y=0
    for p in x:
        y=((y<<5)-y+p)&4294967295
    if y>>31==1:
        return -(4294967296-int(y))
    else:
        return int(y)
def base36(u):
    if u<0:
        return "-"+base36(-u)
    v=""
    while True:
        v="0123456789abcdefghijklmnopqrstuvwxyz"[u%36]+v
        u=int(u/36)
        if u==0:
            break
    return v
def decodestring(x1,x2):
    x1=x1+"="*((-len(x1))%4)
    x2=x2+"="*((-len(x2))%4)
    x1=base64.urlsafe_b64decode(x1.encode("ascii"))
    x2=base64.urlsafe_b64decode(x2.encode("ascii"))
    y=""
    z=(ord(x1[0])+ord(x2[0]))&255
    for i in range(1,len(x2)):
        y+=chr(ord(x1[i])^ord(x2[i])^z)
    return y
def base64encode(x,alphabet):
    x=base64.urlsafe_b64encode(x)
    a={}
    al='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_='
    for i in range(0,len(alphabet)):
        a[al[i]]=alphabet[i]
    return re.sub(".",lambda y: a[y.group()],x)
def base64decode(x,alphabet):
    a={}
    al='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_='
    for i in range(0,len(alphabet)):
        a[alphabet[i]]=al[i]
    x=re.sub(".",lambda y: a[y.group()],x)
    x=x+"="*((-len(x))%4)
    return base64.urlsafe_b64decode(x.encode('ascii'))
STORAGE_OK=3
UUID_TOKEN_KEY="f"
INTEGRITY_KEY="b"
BUNDLE_SEED_KEY="c"
BUNDLE_ID_KEY="d"
FIRMWARE_KEY="z"
PAYLOAD_KEY="a"
class BotDetector:
    def __init__(self):
        self.scriptdata=None
        self.inittime=int(time.time()*1000)
        self.timestamps=[self.inittime+random.randint(40,80),0,random.randint(500,800),random.randint(1000,1500)]
        self.lasteventtime=self.inittime+self.timestamps[2]
        self.bundleseed=None
        self.uuidtoken=None
        self.encryptionseed1=None
        self.encryptionseed2=None
        self.encryptionkey=None
        self.encryptionroundcount=None
        self.headernameprefix=None
        self.plugins=[ -482629523, 916307581, 1078363890 ]
        self.consoleproperties='assert\x00clear\x00context\x00count\x00countReset\x00debug\x00dir\x00dirxml\x00error\x00group\x00groupCollapsed\x00groupEnd\x00info\x00log\x00memory\x00profile\x00profileEnd\x00table\x00time\x00timeEnd\x00timeLog\x00timeStamp\x00trace\x00warn'
        self.fonts=[False,True,False,False,False,False,False,True,False,True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True,False,False,True,False,True,False,True,False,False,True,False,True,False,False,False,False,True,True,False,False]
        self.mathproperties=['abs','acos','acosh','asin','asinh','atan','atanh','atan2','ceil','cbrt','expm1','clz32','cos','cosh','exp','floor','fround','hypot','imul','log','log1p','log2','log10','max','min','pow','random','round','sign','sin','sinh','sqrt','tan','tanh','trunc','E','LN10','LN2','LOG10E','LOG2E','PI','SQRT1_2','SQRT2']
        self.keyevents=[]
        self.mousebuttonevents=[]
        self.animationframetimes=[]
        k=random.randint(820000,900000)
        for i in range(0,10):
            self.animationframetimes.append(round(float(k)/1000,3))
            k+=random.randint(16660,16700)
        self.visibilityevents=[]
        self.mousemoveevents={"recent":[],"throttled":[]}
        self.mediadeviceids=["communications",os.urandom(32).encode('hex'),os.urandom(32).encode('hex'),"communications",os.urandom(32).encode('hex')]
        self.browserdata={"global":{"innerHeight":969,"innerWidth":1920,"outerHeight":1040,"outerWidth":1920,"screenX":0,"screenY":0,"isSecureContext":True,"devicePixelRatio":1},"screen":{"height":1080,"width":1920,"availHeight":1040,"availWidth":1920,"pixelDepth":24,"colorDepth":24},"navigator":{"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36","buildID":None,"cpuClass":None,"hardwareConcurrency":12,"maxTouchPoints":0,"platform":"Win32","product":"Gecko","productSub":"20030107","oscpu":None,"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36","vendor":"Google Inc.","vendorSub":"","doNotTrack":None,"webdriver":False},"operaVersion":None,"toolbar":True,"locationbar":True}
        self.devicedata={"parameters":{"antialias":True,"maxAnisotropy":16,"dimensions":["11","11024","3276732767"],"params":{"alphaBits":8,"blueBits":8,"greenBits":8,"redBits":8,"depthBits":24,"maxCombinedTextureImageUnits":32,"maxCubeMapTextureSize":16384,"maxFragmentUniformVectors":1024,"maxRenderbufferSize":16384,"maxTextureImageUnits":16,"maxTextureSize":16384,"maxVaryingVectors":30,"maxVertexAttribs":16,"maxVertexTextureImageUnits":16,"maxVertexUniformVectors":4096,"renderer":"WebKit WebGL","shadingLanguageVersion":"WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)","stencilBits":0,"vendor":"WebKit","version":"WebGL 1.0 (OpenGL ES 2.0 Chromium)"},"debugInfo":{"vendor":"Google Inc.","renderer":"ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)"}},"shaderPrecisions":["23127127","23127127","23127127","23127127","23127127","23127127","03130","03130","03130","03130","03130","03130"],"supportedExtensions":["ANGLE_instanced_arrays","EXT_blend_minmax","EXT_color_buffer_half_float","EXT_disjoint_timer_query","EXT_float_blend","EXT_frag_depth","EXT_shader_texture_lod","EXT_texture_filter_anisotropic","WEBKIT_EXT_texture_filter_anisotropic","EXT_sRGB","KHR_parallel_shader_compile","OES_element_index_uint","OES_standard_derivatives","OES_texture_float","OES_texture_float_linear","OES_texture_half_float","OES_texture_half_float_linear","OES_vertex_array_object","WEBGL_color_buffer_float","WEBGL_compressed_texture_s3tc","WEBKIT_WEBGL_compressed_texture_s3tc","WEBGL_compressed_texture_s3tc_srgb","WEBGL_debug_renderer_info","WEBGL_debug_shaders","WEBGL_depth_texture","WEBKIT_WEBGL_depth_texture","WEBGL_draw_buffers","WEBGL_lose_context","WEBKIT_WEBGL_lose_context"],"contextProperties":-368668372}
    def processrawscript(self,x):
        funcstr=re.search("function a\(b\)({.*?)\n",x).group(1)
        funcstr=funcstr[:funcstr.rfind("}")]
        self.scriptdata={"length":len(funcstr),"whitespace":len(re.findall('\s',funcstr)),"punctuators":len(re.findall('[.{([,;=/]',funcstr))}
        m=re.search(" H=(.*?);",x).group(1)
        mm=eval(m)
        m=mm.index("o_0")
        m=chr(m>>8)+chr(m&255)
        k=re.search("bo=M\(\"(.*?)\"",x).group(1)
        k=k+"="*((-len(k))%4)
        k=base64.urlsafe_b64decode(k.encode('ascii'))
        i=0
        while i<len(k):
            j=k.find(m,i)
            i+=1
            if j==-1:
                raise Exception("Failed to extract bundle seed")
            l=[ord(k[s])<<8|ord(k[s+1]) for s in range(max(0,j-100),j+100)]
            l=[mm[p] for p in l if p<len(mm)]
            l=[p for p in l if len(p)>118]
            if len(l)<2: continue
            self.bundleseed=decodestring(l[0],l[1])
            break
        l=re.search("initCustomEvent\(.*?\[\"(.*?)\",\"(.*?)\".*?,.*?,(.*?\])",x)
        self.uuidtoken,self.alphabet=l.group(1),l.group(2)
        self.encryptionkey=eval(l.group(3))
        bm=re.search("var K=(.*?);",funcstr).group(1)
        fns=json.loads(re.search("var J=(.*?);",funcstr).group(1))
        ls=eval(re.search("var L=(.*?);",funcstr).group(1))
        enf,eng=re.findall("{.:([0-9]*?),.:([0-9]*?),",bm)[3]
        v=funcstr.find("var dB=")
        vdb=funcstr[v:funcstr.find("];function",v)]
        vdb=vdb.split(",function(")
        lfunc=[i for i in range(0,len(vdb)) if "=L[" in vdb[i]][0]
        prfunc=[i for i in range(0,len(vdb)) if re.search("\..\..;",vdb[i])][0]
        afunc=[i for i in range(0,len(vdb)) if vdb[i].count(";A(")==1][0]
        mfunc=[i for i in range(0,len(vdb)) if "(-" in vdb[i]][0]
        lsfunc=[i for i in range(0,len(vdb)) if "<<" in vdb[i]][0]
        pcfunc=[i for i in range(0,len(vdb)) if "%" in vdb[i]][0]
        vdbn=[sum(int(q) for q in re.findall("\..([1-3])\(",p)) for p in vdb]
        lvals=[]
        j=int(enf)
        g=int(eng)
        enck=[]
        encs=None
        p=None
        count=0
        while len(enck)<4 and count<200:
            count+=1
            [g,s]=fns[g][ord(k[j])]
            j+=1
            if s==prfunc:
                j=p[0]
                g=p[1]
            elif vdbn[s]==3:
                p=(j+3,g)
                j,g=ord(k[j])<<8|ord(k[j+1]),ord(k[j+2])
            elif vdbn[s]==4:
                p=(j+4,g)
                j,g=ord(k[j])<<16|ord(k[j+1])<<8|ord(k[j+2]),ord(k[j+3])
            elif s==afunc:
                enck.append(lvals.pop())
            elif s==mfunc:
                lvals[-1]=-lvals[-1]
            elif s==lfunc:
                if encs==None:
                    encs=ls[ord(k[j])]
                else:
                    lvals.append(ls[ord(k[j])])
                j+=1
            else:
                j+=vdbn[s]
        if len(enck)<4:
            raise Exception("Failed to extract encryption seed")
        gate=[True,True]
        ls=0
        while True:
            [g,s]=fns[g][ord(k[j])]
            j+=1
            if vdbn[s]>=3 and "if" in vdb[s]:
                if len(gate)==0: raise Exception("Unknown if")
                l=gate.pop(0)
                if "if(!" in vdb[s]: l=not l
                if l:
                    if vdbn[s]==3:
                        j,g=ord(k[j])<<8|ord(k[j+1]),ord(k[j+2])
                    else:
                        j,g=ord(k[j])<<16|ord(k[j+1])<<8|ord(k[j+2]),ord(k[j+3])
                else:
                    j+=vdbn[s]
            elif vdbn[s]==3:
                p=(j+3,g)
                j,g=ord(k[j])<<8|ord(k[j+1]),ord(k[j+2])
            elif vdbn[s]==4:
                p=(j+4,g)
                j,g=ord(k[j])<<16|ord(k[j+1])<<8|ord(k[j+2]),ord(k[j+3])
            elif s==prfunc:
                j=p[0]
                g=p[1]
            elif s==lsfunc:
                ls+=1
            elif s==pcfunc:
                break
            else:
                j+=vdbn[s]
        self.encryptionroundcount=ls/32
        self.encryptionseed1=enck
        self.encryptionseed2=encs
    def encode(self,data):
        iv1=random.getrandbits(32)
        iv2=random.getrandbits(32)
        data=encrypt(self.encryptionkey,data,iv1,iv2,self.encryptionseed1,self.encryptionseed2,self.encryptionroundcount)
        data="".join(chr(p) for p in data)
        iv=[iv1>>24,iv1>>16&255,iv1>>8&255,iv1&255,iv2>>24,iv2>>16&255,iv2>>8&255,iv2&255]
        iv="".join(chr(p) for p in iv)
        return base64encode(struct.pack(">I",iv1)+struct.pack(">I",iv2)+data,self.alphabet)
    def decode(self,data):
        data=base64decode(data,self.alphabet)
        iv1=struct.unpack(">I",data[:4])[0]
        iv2=struct.unpack(">I",data[4:8])[0]
        data=encrypt(self.encryptionkey,[ord(data[i]) for i in range(8,len(data))],iv1,iv2,self.encryptionseed1,self.encryptionseed2,self.encryptionroundcount)
        return data
    def generateevents(self):
        x=int(time.time()*1000)
        maxbevents=random.randint(4,8)
        tl=self.lasteventtime
        startx=random.randint(300,1900)
        starty=random.randint(100,900)
        movex=1
        movey=1
        while (x-tl)>1000 and maxbevents>0:
            s=random.randint(500,(x-tl)/2)
            k=random.randint(5,10)
            tl+=s
            while len(self.mousemoveevents["recent"])<32 and k>0:
                tl+=random.randint(30,50)
                self.mousemoveevents["recent"].append({"eventType":4,"timestamp":(tl-self.inittime),"x":startx,"y":starty})
                startx+=random.randint(10,50)*movex
                starty+=random.randint(10,50)*movey
                if startx<300 or startx>1900:
                    movex=-movex
                    startx+=random.randint(10,50)*movex
                if starty<100 or starty>1000:
                    movey=-movey
                    starty+=random.randint(10,50)*movey
                k-=1
            tl+=random.randint(10,50)
            self.mousebuttonevents.append({"button":0,"eventType":3,"sequenceNumber":0,"target":{"id":'',"name":UNDEFINED,"nodeType":1,"tagName":'LABEL' },"timestamp":(tl-self.inittime),"x":startx,"y":starty})
            startx+=random.randint(10,50)*movex
            starty+=random.randint(10,50)*movey
            if startx<300 or startx>1900:
                movex=-movex
                startx+=random.randint(10,50)*movex
            if starty<100 or starty>1000:
                movey=-movey
                starty+=random.randint(10,50)*movey
            maxbevents-=1
    def generatedata(self):
        self.timestamps[-1]=int(time.time()*1000)-self.inittime
        signals=[]
        signals.append(["0",{"timestamp":self.inittime}])
        signals.append(["5",18446744073709550000]) # parseInt('0xFFFFFFFFFFFFFBFF',16)
        signals.append(["7",{"hasDefaultBrowserHelper":False,"hasWidevinePlugin":False,"plugins":self.plugins}]) #plugin data for chrome
        signals.append(["11",{"dataFragment":'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwA',"hashcode":1037736760}]) # canvas fingerprint, text 'Hel$&?6%){mZ+#@'
        signals.append(["12",False]) # chrome.webstore
        signals.append(["13",False]) # checking window.Image
        signals.append(["14",simplehash(self.consoleproperties)]) # checking properties of the object window.console
        signals.append(["15",{"hasToSource":False,"sourceHash":0,"stringHash":simplehash("function createElement() { [native code] }")}]) # hash of document.createElement.toString()
        signals.append(["21",'Sun Aug 05 1945 19:16:00 GMT-0400 (Eastern Daylight Time)']) # new Date(-770172240000).toString()
        signals.append(["24",{"fonts":self.fonts,"version":5}])
        signals.append(["25",{"callable":True,"documentElement":True,"exists":True,"falsy":True,"nullish":True,"type":"undefined"}]) # properties of document.documentElement
        signals.append(["29",[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]])
        signals.append(["32",{"emptyReferrer":True,"historyLength":2}])
        signals.append(["34",True]) # typeof indexedDB.open == "function"
        signals.append(["39",self.keyevents])
        signals.append(["42",{"hash":simplehash("\x00".join(self.mathproperties)),"mathProperties":self.mathproperties}])
        signals.append(["45",[simplehash(p) for p in self.mediadeviceids]])
        signals.append(["47",{"mouseButtonEvents":self.mousebuttonevents,"mouseMoveEvents":self.mousemoveevents}])
        signals.append(["48",{"argumentsValue":'{"0":{"isTrusted":false}}',"hasArguments":True,"hasGlobal":False,"hasProcess":False}])
        signals.append(["51",{"avgAlpha":None,"avgBeta":None,"avgGamma":None,"avgInterval":0,"numOrientationEvents":1,"stdDevAlpha":0,"stdDevBeta":0,"stdDevGamma":0,"stdDevInterval":0}])
        signals.append(["57",{"statuscode":STORAGE_OK,"value":self.uuidtoken}])
        signals.append(["59",{"global":{"ActiveXObject":False,"ApplePaySession":False,"File":True,"MutationObserver":True,"Notification":True,"SharedWorker":True,"TouchEvent":True,"XDomainRequest":False,"_phantom":False,"attachEvent":False,"callPhantom":False,"createPopup":False,"detachEvent":False,"event":True,"external":True,"fireEvent":False,"frameElement":True,"globalStorage":False,"localStorage":True,"mozRTCPeerConnection":False,"mozRequestAnimationFrame":False,"phantom":False,"postMessage":True,"PushManager":True,"registerProtocolHandler":False,"requestAnimationFrame":True,"sessionStorage":True,"sidebar":False,"webkitRequestAnimationFrame":True,"webkitResolveLocalFileSystemURL":True,"webkitRTCPeerConnection":True,"BluetoothUUID":True,"netscape":False,"__fxdriver_unwrapped":False,"_Selenium_IDE_Recorder":False},"document":{"_Selenium_IDE_Recorder":False,"all":True,"characterSet":True,"charset":True,"compatMode":True,"documentMode":False,"images":True,"layers":False,"$cdc_asdjflasutopfhvcZLmcfl_":False,"__fxdriver_unwrapped":False,"__webdriver_script_fn":False},"documentBody":{"contextMenu":False,"innerText":False,"mozRequestFullScreen":False,"requestFullScreen":False,"webkitRequestFullScreen":False},"navigator":{"vibrate":True,"webdriver":False,"credentials":True,"storage":True,"requestMediaKeySystemAccess":True,"bluetooth":True},"crypto":{"subtle":True},"external":{"Sequentum":False}}])
        signals.append(["60",self.browserdata])
        signals.append(["61",self.animationframetimes]) # 10 consecutive requestAnimationFrame
        signals.append(["97",{"afterReady":{"InstallTrigger":True,"controllers":True},"immediately":{"InstallTrigger":True,"controllers":True},"lastChance":{"InstallTrigger":True,"controllers":True}}])
        signals.append(["99",{"bodyAttribute":False,"scriptPresent":False}])
        signals.append(["102",{"description":UNDEFINED,"message":"Cannot read property '0' of null","name":"TypeError","num":UNDEFINED,"stack":"TypeError: Cannot read property '0' of null\n    at URL","stacktrace":UNDEFINED}])
        signals.append(["104",self.scriptdata])
        signals.append(["106",self.timestamps])
        signals.append(["109",[]])
        signals.append(["110",False])
        signals.append(["111",{"mpeg":"probably","x-mpeg":"","x-mpegurl":"","mp4":"maybe","mp4; codecs=mp4a.40.2":"probably","ogg; codecs=opus":"probably","ogg; codecs=speex":"","webm; codecs=vorbis":"probably","wav; codecs=\"0\"":"","wav; codecs=\"1\"":"probably","wav; codecs=\"2\"":"","wave":"","wave; codecs=0":"","wave; codecs=1":"","wave; codecs=2":"","3gpp; codecs=\"mp4v.20.8, samr\"":"","webm; codecs=\"vorbis,vp9\"":"probably","mp4; codecs=\"avc1.42c00d\"":"probably","webm; codecs=\"vp8, vorbis\"":"probably","ogg; codecs=theora":"probably","ogg; codecs=\"theora, speex\"":"","mp4; codecs=\"avc1.64001E, mp4a.40.2\"":"probably","mp4; codecs=\"mp4v.20.8, mp4a.40.2\"":"","mp4; codecs=bogus":"","mp2t; codecs=\"avc1.42E01E,mp4a.40.2\"":""}])
        signals.append(["112",{"events":self.visibilityevents,"finalState":True,"initialState":True,"visibilityEventCount":len(self.visibilityevents)}])
        signals.append(["113",self.devicedata])
        signals.append(["116",[]])
        signals.append(UNDEFINED)
        signals.append(["custom_ChromeConsole",False])
        data=Encoder().encode({"errors":[],"signals":signals},[["timestamp"],["channelCount","channelCountMod","channelInterpretation","fftSize","frequencyBinCount","maxChannelCount","maxDecibels","minDecibels","numberOfInputs","numberOfOutputs","sampleRate","smoothingTimeConstant","state"],["hash","max","min"],["audio/mpeg","audio/ogg","audio/wav","audio/wave","audio/webm"],["hasDefaultBrowserHelper","hasWidevinePlugin","plugins"],["dataFragment","hashcode"],["hasToSource","sourceHash","stringHash"],["computedStyleHash"],["background-repeat: round space;","border-image: none;","border-radius: 4px;","color: var(companyblue);","display: run-in;","filter: blur(2px);","flow-into: main-thread;","grid-columns: auto 1fr;","hyphens: auto;","inline-block: none;","mask-repeat: repeat-x;","mask: auto;","object-fit: contain;","overflow-scrolling: touch;","position: sticky;","resize: both;","tab-size: 4;","text-stroke: 2.0px;","user-select: none;","word-break: auto;"],["","-moz-","-ms-","-webkit-"],["-moz-osx-font-smoothing","-webkit-app-region","-webkit-text-size-adjust","animation","column-count","hyphens","justify-items","text-align-last","text-emphasis","text-orientation"],["caughtException","userAgentStyleHash"],[],["global"],["pageXOffset","pageYOffset"],["fonts","version"],["callable","documentElement","exists","falsy","nullish","type"],["foreignElements","links"],["innerText","tagName","xpath"],["d83d-dc69-d83c-dffb-200d-2764-fe0f-200d-d83d-dc69-d83c-dffe","d83d-dd2b","d83d-ddfe","d83d-decd","d83e-dd16","d83e-dd8b"],["alpha","colors"],["avg","count","volume"],["b","g","r"],["emptyReferrer","historyLength"],["completeness","id","seen"],["keyDown","keyPress","keyUp"],["altKey","ctrlKey","eventType","instanceOfUIEvent","keyCode","markedAsTrusted","metaKey","sequenceNumber","shiftKey","target","timestamp"],["eventType","keyCode","modifierKeys","sequenceNumber","target","timestamp"],["language","languages"],["hash","mathProperties"],["mouseClick","mouseDown","mouseMove","mouseUp"],["button","eventType","instanceOfUIEvent","markedAsTrusted","oX","oY","sequenceNumber","target","timestamp","x","y"],["button","eventType","instanceOfUIEvent","markedAsTrusted","target","timestamp","x","y"],["mouseButtonEvents","mouseMoveEvents"],["button","eventType","sequenceNumber","target","timestamp","x","y"],["recent","throttled"],["eventType","timestamp","x","y"],["argumentsValue","hasArguments","hasGlobal","hasProcess"],["nonce"],["avgAlpha","avgBeta","avgGamma","avgInterval","numOrientationEvents","stdDevAlpha","stdDevBeta","stdDevGamma","stdDevInterval"],["connectStart","domComplete","domContentLoadedEventEnd","domContentLoadedEventStart","domInteractive","domLoading","loadEventEnd","loadEventStart","requestStart","responseEnd","responseStart"],["statuscode","value"],["document","documentBody","external","global","navigator"],["ActiveXObject","ApplePaySession","File","Int8Array","MutationObserver","Notification","PushManager","SharedWorker","TouchEvent","XDomainRequest","_Selenium_IDE_Recorder","__fxdriver_unwrapped","_phantom","addEventListener","attachEvent","awesomium","callPhantom","createPopup","detachEvent","dispatchEvent","domAutomationController","event","external","fireEvent","frames","getComputedStyle","globalStorage","localStorage","mozRTCPeerConnection","mozRequestAnimationFrame","phantom","postMessage","registerProtocolHandler","removeEventListener","requestAnimationFrame","sessionStorage","sidebar","webkitRTCPeerConnection","webkitRequestAnimationFrame","webkitResolveLocalFileSystemURL"],["$cdc_asdjflasutopfhvcZLmcfl_","_Selenium_IDE_Recorder","__fxdriver_unwrapped","__webdriver_script_fn","all","characterSet","charset","compatMode","documentMode","getElementById","getElementsByClassName","hasAttributes","images","layers","querySelector"],["contextMenu","innerHTML","innerText","mozRequestFullScreen","requestFullScreen","webdriver","webkitRequestFullScreen"],["vibrate"],["Sequentum"],["crypto","document","documentBody","external","global","navigator"],["ActiveXObject","ApplePaySession","BluetoothUUID","File","MutationObserver","Notification","PushManager","SharedWorker","TouchEvent","XDomainRequest","_Selenium_IDE_Recorder","__fxdriver_unwrapped","_phantom","attachEvent","callPhantom","createPopup","detachEvent","event","external","fireEvent","frameElement","globalStorage","localStorage","mozRTCPeerConnection","mozRequestAnimationFrame","netscape","phantom","postMessage","registerProtocolHandler","requestAnimationFrame","sessionStorage","sidebar","webkitRTCPeerConnection","webkitRequestAnimationFrame","webkitResolveLocalFileSystemURL"],["$cdc_asdjflasutopfhvcZLmcfl_","_Selenium_IDE_Recorder","__fxdriver_unwrapped","__webdriver_script_fn","all","characterSet","charset","compatMode","documentMode","images","layers"],["contextMenu","innerText","mozRequestFullScreen","requestFullScreen","webkitRequestFullScreen"],["bluetooth","credentials","requestMediaKeySystemAccess","storage","vibrate","webdriver"],["subtle"],["global","locationbar","navigator","operaVersion","screen","toolbar"],["devicePixelRatio","innerHeight","innerWidth","isSecureContext","outerHeight","outerWidth","screenX","screenY"],["availHeight","availWidth","colorDepth","height","pixelDepth","width"],["appCodeName","appName","appVersion","buildID","cpuClass","doNotTrack","hardwareConcurrency","maxTouchPoints","oscpu","platform","product","productSub","userAgent","vendor","vendorSub","webdriver"],["ip","model"],["constructor","lastChance"],["events"],["accuracy","timestamp","x","y","z"],["level","powerSource","status","technology","temp","voltage"],["androidId","board","deviceBrand","deviceModel","deviceModelNumber","hardware","hardwareName","manufacturer","osBuildFingerprint","osBuildNumber","osName","osVersion","product","serial"],["availableRam","availableStorage","totalRam","totalStorage"],["bignox","bluestacks","genymotion","superuser"],["kernelPatch"],["country","currency","language","timezone"],["accuracy","distance","timestamp"],["density","height","width"],["configId","errorArray","kernelId","kernelURI","kernelUpdateHeaderName","lastErrorCount","lastErrorId","lastErrorTimestamp","timeSinceLastRequest"],["jvmVersion","osArch","osName","osVersion"],["timestamp","x","y","z"],["level","status"],["appBundleName","appInstallId","appVersion","cfBundleInfo","deviceBrand","deviceModel","deviceModelNumber","intAppVersion","osType","osVersion","sdkVersion"],["availableStorage","numCores","timestamp","totalRam","uptimeSinceBoot"],["brightness","density","height","width"],["hw.cputype","hw.model","hw.physicalcpu","kern.boottime","kern.hostname","kern.proc","kern.version"],["appdir"],["jailbreak"],["data","mnt","storage"],["eth0","p2p0","wlan0"],["root"],["cpuinfo","date","uname","whoami"],["net.hostname","ro.boot.boottime","ro.build.date.utc","ro.build.fingerprint","ro.runtime.firstboot","serialno"],["afterReady","immediately","lastChance"],["InstallTrigger","controllers"],["status","value"],["bodyAttribute","scriptPresent"],["hash"],["description","message","name","num","stack","stacktrace"],["length","punctuators","whitespace"],["touchEnd","touchMove","touchStart"],["eventType","timestamp","touches"],["oX","oY","x","y"],["x","y"],["3gpp; codecs=\"mp4v.20.8, samr\"","mp2t; codecs=\"avc1.42E01E,mp4a.40.2\"","mp4","mp4; codecs=\"avc1.42c00d\"","mp4; codecs=\"avc1.64001E, mp4a.40.2\"","mp4; codecs=\"mp4v.20.8, mp4a.40.2\"","mp4; codecs=bogus","mp4; codecs=mp4a.40.2","mpeg","ogg; codecs=\"theora, speex\"","ogg; codecs=opus","ogg; codecs=speex","ogg; codecs=theora","wav; codecs=\"0\"","wav; codecs=\"1\"","wav; codecs=\"2\"","wave","wave; codecs=0","wave; codecs=1","wave; codecs=2","webm; codecs=\"vorbis,vp9\"","webm; codecs=\"vp8, vorbis\"","webm; codecs=vorbis","x-mpeg","x-mpegurl"],["events","finalState","initialState","visibilityEventCount"],["timestamp","visible"],["contextProperties","parameters","shaderPrecisions","supportedExtensions"],["antialias","debugInfo","dimensions","maxAnisotropy","params"],["alphaBits","blueBits","depthBits","greenBits","maxCombinedTextureImageUnits","maxCubeMapTextureSize","maxFragmentUniformVectors","maxRenderbufferSize","maxTextureImageUnits","maxTextureSize","maxVaryingVectors","maxVertexAttribs","maxVertexTextureImageUnits","maxVertexUniformVectors","redBits","renderer","shadingLanguageVersion","stencilBits","vendor","version"],["renderer","vendor"],["candidate","ip"],["hasSpeechSynthesis","voiceData"],["hash","match","noOfDefaultVoices","noOfVoices","relLang","relVoiceUri"],["bursts","events"],["errors","signals"]])
        return self.encode(data)
    def getheaders(self):
        x={}
        x[self.headernameprefix+UUID_TOKEN_KEY]=self.uuidtoken
        x[self.headernameprefix+BUNDLE_ID_KEY]="o_0"
        x[self.headernameprefix+BUNDLE_SEED_KEY]=self.bundleseed
        m=self.generatedata()
        x[self.headernameprefix+PAYLOAD_KEY]=m
        x[self.headernameprefix+INTEGRITY_KEY]=base36(simplehash(self.uuidtoken+m))
        x[self.headernameprefix+FIRMWARE_KEY]="p"
        return x