/**
 *  Main client JavaScript container
 *  @author Una Ada (Trewbot) <una@phene.co>
 */

window._c = function(c){return document.getElementsByClassName(c);}
Element.prototype._c = function(c){return this.getElementsByClassName(c);}
//  Abbreviated function for HAndlebars template compiling
window._h = function(i){return Handlebars.compile(_i('template__'+i).innerHTML)};
window._i = function(i){return document.getElementById(i);}

//  Resize an element to show all of its content
Element.prototype.fitContent = function(){
    var l = ['change','cut','paste','drop','keydown'];
    for(var i in l) this.addEventListener(l[i], resize.bind(this), !1);
}
window.resize = function(){
    window.setTimeout((function(){
        var t = this,
            c = t.cloneNode();
        t.parentNode.insertBefore(c, t);
        c.style.height = 'auto';
        c.value = t.value;
        t.style.height = (c.scrollTop + c.scrollHeight + 20) + 'px';
        t.parentNode.removeChild(c);
    }).bind(this), 0);
}

//  Render a responder element to show click responses
Element.prototype.responsibleParent = function(){
    var t = this;
    if(t == null)
        return false;
    try{
        while(t.tagName.toLowerCase() !== 'html'){
            if(~t.className.indexOf('has-responder'))
                return t;
            t = t.parentElement;
        }
    }catch(e){}
    return false;
}
window.lastClick = {x:0,y:0};   // initialize mouse click position register
window.addEventListener('click',function(e){
    window.lastClick.x = e.pageX;
    window.lastClick.y = e.pageY;
    var rsp = e.target.responsibleParent();
    if(rsp){
        var rpr = rsp._c('responder')[0],
            rct = rsp.getBoundingClientRect(),
            xPos = e.clientX - rct.left,
            yPos = e.clientY - rct.top,
            rad = Math.sqrt(Math.pow(rct.width,2) + Math.pow(rct.height,2));
        rpr.style.transition = "";
        rpr.style.webkitClipPath = "circle(0% at "+xPos+"px "+yPos+"px)";
        rpr.style.opacity = 1;
        window.setTimeout(function(){
            rpr.style.transitionDuration = "1.0s";
            rpr.style.webkitClipPath = "circle(" + rad + "px at "+xPos+"px "+yPos+"px)";
            rpr.style.opacity = 0;
        },10);
    }
});

//  Inserts text in a textarea elements at the caret
HTMLTextAreaElement.prototype.insertAtCaret = function(text){
    text = text || '';
    if(document.selection){
        this.focus();
        var sel		= document.selection.createRange();
        sel.text	= text;
    }else if(this.selectionStart || this.selectionStart === 0){
        var start	= this.selectionStart,
            end		= this.selectionEnd;
        this.value = this.value.substring(0, start) + text + this.value.substring(end, this.value.length);
        this.selectionStart = start + text.length;
        this.selectionEnd = start + text.length;
    }else this.value += text;
};
//  Some Handlebars shit that should really exist by default
Handlebars.registerHelper('ifCond', function(u,s,v,o){
    return eval(u + s + v) ? o.fn(this) : o.inverse(this);
});
Handlebars.registerHelper('strCompare', function(u,v,o){
    return u == v ? o.fn(this) : o.inverse(this);
});
//  Collect all the element of several objects into a single object
Object.collect= function(){
    var ret = {},
        len = arguments.length;
    for(var i = 0; i < len; i++)
        for(p in arguments[i])
            if(arguments[i].hasOwnProperty(p))
                ret[p] = arguments[i][p];
    return ret;
};
//  Find the module that contains a certain element
Element.prototype.parentModule = function(){
    var t = this;
    if(t == null)
        return false;
    try{
        while(t.tagName.toLowerCase() !== 'html'){
            if(t.classList.contains('module'))
                return t;
            t = t.parentElement;
        }
    }catch(e){}
    return false;
}

/**
 *  Namespace for client scripts (abbreviated as _ci)
 *  @namespace CollectiveIntelligence
 */
_ci         = (CollectiveIntelligence = new(function(){
    /**
     *  @function time
     *  @arg {Number} unix Unix timestamp in milliseconds.
     *  @arg {Boolean} HE Toggle using Human Era dates.
     *  @return {String} Abbreviated string describing the relative date.
     */
    this.time	= function(unix, HE=!1){
        var ago = ~~(+new Date/1e3)-(unix/1e3),
            num = {1:'',60:' second',3600:' minute',
                    86400:' hour',2678400:' day'},
            k	= Object.keys(num),
            s;
        for(var i in num)
            if(ago<+i) return ago>0
                ?(s=~~(ago/k[k.indexOf(""+i)-1]))+num[i]+(s!=1?'s':'')
                :'Right Now!';
        var stamp = new Date(+unix);
        return ['Jan','Feb','Mar','Apr','May','Jun',
                'Jul','Aug','Sep','Oct','Nov','Dec'][stamp.getMonth()]
                +' '+stamp.getDate()+', '+(stamp.getFullYear()+(HE?1e4:0));
    };

    /*
     *  Update any element with className "timestamp" as a timestamp; elements
     *  should have a "unix-time" attribute with a unix time in milliseconds.
     */
    setInterval(function(){
        var ts = document.getElementsByClassName('timestamp');
        for(let i in ts)
            if(typeof ts[i].getAttribute == 'function'
            && !isNaN(parseInt(ts[i].getAttribute('unix-time'))))
                ts[i].innerHTML = _ci.time(ts[i].getAttribute('unix-time'));
    },1e3);
})());
_ci.tp      = (_ci.templates = {    //  Handlebars templates
    //account     : _h('account'),
    //curation    : _h('curation'),
    //delegation  : _h('delegation'),
    //dropdown    : _h('dropdown'),
    //dropdown2   : _h('dropdown2'),
    sidebar     : _h('sidebar'),
    //tokens      : _h('tokens'),
    test        : _h('test')
});
_ci.m       = (_ci.modules = {      //  Module information
    test1   : {
        name: "Test Module 1",
        template: _ci.tp.test
    },
    test2   : {
        name: "Test Module 2",
        template: _ci.tp.test
    },
    test3   : {
        name: "Test Module 3",
        template: _ci.tp.test
    },
    test4   : {
        name: "Test Module 4",
        template: _ci.tp.test
    },
    test5   : {
        name: "Test Module 5",
        template: _ci.tp.test
    },
    test6   : {
        name: "Test Module 6",
        template: _ci.tp.test
    }
});
_ci.t       = (_ci.theme = {        //  Maniplate the page theme
    darkMode      : false,          //  If dark mode is set
    isMenuOpen    : false,          //  If sidebar menu is open
    menu(){                         //  Toggle sidebar menu open/close
        _c("side")[0].style.left = !(this.isMenuOpen = !this.isMenuOpen)
            ?"-220px"
            :"-20px";
        _c("side")[0].style.transitionTimingFunction = !this.isMenuOpen
            ? "cubic-bezier(0.7, 0.0, 1.0, 1.0)"
            : "cubic-bezier(0.5, 0.0, 0.0, 1.5)";
    },
    /**
     *  @function t.setDarkMode Set UI theme (light, dark)
     *  @arg {Boolean} darkMode Whether or not to set as Dark Mode
     */
    setDarkMode(darkMode){
        _ci.t.darkMode = darkMode;
        _ci.ui.update();
    },
    side(ctx,next){
        _ci.u.getSession(function(sess){
            _ci.session = sess;
            var o = {
                sections: [
                    {
                        links: [
                            {
                                name: "Dashboard",
                                url: "/"
                            },
                            {
                                name: "Curation",
                                url: "/curation"
                            },
                            {
                                name: "Goups",
                                url: "/groups"
                            },
                            {
                                name: "Debates",
                                url: "/debates"
                            },
                            {
                                name: "Delegations",
                                url: "/delegations"
                            },
                            {
                                name: "Rewards",
                                url: "/rewards"
                            },
                            {
                                name: "Account",
                                url: "/account"
                            },
                            {
                                name: "Settings",
                                url: "/settings"
                            }
                        ]
                    }
                ]
            };
            _c('side__content')[0].innerHTML = _ci.tp.sidebar(o);
            next();
        });
    },
    /**
     *  @function t.toggleDarkMode Toggle dark mode
     */
    toggleDarkMode(){
        _ci.t.setDarkMode(!_ci.t.darkMode);
    }
});
_ci.u       = (_ci.users = {        //  Account information and interaction
    /**
     *  @function getSession
     *  @arg {Function} next Callback function, should have
     *  @return {Object} Object containing data about current session
     */
    getSession(next){
        next({});
    }
});
_ci.ui      = (_ci.interface = {    //  User interface rendering and events
    register : {},
    editing : false,
    /*
     *  Default column arrangement, overridden by user settings
     *      `center` if the column should be centered in the screen, only one
     *          column can have this flag, ignored if the total width of all
     *          columns is wider than the screen
     *      `contains` an array of all modules contained in the column
     *      `width` the width of the column in pixels
     */
    columns : [
        {
            contains: [
                "test1",
                "test2",
                "test3"
            ],
            width: 300
        },
        {
            center: true,
            contains: [
                "test4"
            ],
            width: 500
        },
        {
            contains: [
                "test5",
                "test6"
            ],
            width: 300
        }
    ],
    //  Module dragging functions and variables
    moduleDrag : {
        after : false,
        column : -1,
        offsets : {x:0,y:0}, // Position on element being dragged
        target : 0, // Element of module being dragged
        timer : 0, // Timer id stored for convenience
        width: 0, // Original width of module
        /**
         *  @function ui.moduleDrag.mouseDown Start dragging if editing is true
         *  @arg {Event} e mouseDown event
         */
        mouseDown(e){
            if(!_ci.ui.editing) return;
            //  Add event listeners
            window.addEventListener("mousemove",_ci.ui.moduleDrag.drag);
            window.addEventListener("mouseup",_ci.ui.moduleDrag.endDrag);
            document.getElementsByTagName("body")[0].classList.add("is-dragging");
            //  Set up module element for dragging
            let el = e.target.parentModule(),
                br = el.getBoundingClientRect();
            el.style.left = br.left + "px";
            el.style.top = br.top + "px";
            el.style.width = br.width + "px";
            el.classList.add("is-lifted");
            el.classList.add("is-dragging");
            //  Set variables for dragging
            let moduleid = el.getAttribute("moduleid");
            _ci.ui.moduleDrag.offset = {
                x: e.pageX-br.left,
                y: e.pageY-br.top
            };
            _ci.ui.moduleDrag.target = el;
            _ci.ui.moduleDrag.width = br.width;
            _ci.ui.moduleDrag.targetId = moduleid;
            _ci.ui.moduleDrag.column = _ci.ui.register[moduleid].frame.parentNode.id.split("-")[1];
            _ci.ui.register[moduleid].frame.classList.add("is-empty");
        },
        /**
         *  @function ui.moduleDrag.startDrag Handler for dragging modules
         */
        startDrag(){
        },
        /**
         *  @function ui.moduleDrag.drag Handle dragging module
         *  @arg {Event} e movemouse event
         */
        drag(e){
            let el = _ci.ui.moduleDrag.target;
            el.style.width = _ci.ui.moduleDrag.width + "px";
            for(let i in _ci.ui.columns){
                let br = _i("column-"+i).getBoundingClientRect();
                if(e.pageX + scrollX> br.left && e.pageX + scrollX < br.left + br.width){
                    //  Set module width to current target column width
                    el.style.width = _ci.ui.columns[i].width + "px";
                    //  Determine target position in column
                    let mf = _i("column-"+i)._c("mFrame"),
                        af = false;
                    //  Loop through current columns
                    for(let j of mf){
                        //  Ignore empty frames so it doesn't just go after itself
                        if(j.classList.contains("is-empty")) continue;
                        let br2 = j.getBoundingClientRect();
                        //  Check if target position is after this frame
                        if(e.pageY + scrollY >= br2.top + (br2.height/2))
                            af = j;
                        //  If it isn't after the current frame stop checking
                        else break;
                    }
                    if((!af && _ci.ui.moduleDrag.column !== i) || af !== _ci.ui.moduleDrag.after){
                        let mel = document.createElement("div"),
                            col = _i("column-"+i);
                        mel.classList.add("mFrame");
                        mel.classList.add("is-empty");
                        //mel.style.height = 0;
                        //  If not after anything instert empty frame as first child
                        if(af == false)
                            col.insertBefore(mel,col.firstChild);
                        //  If after a frame insert empty frame after that frame
                        else
                            col.insertBefore(mel,af.nextSibling);
                        _ci.ui.moduleDrag.after = af;
                        _ci.ui.moduleDrag.column = i;
                        _ci.ui.register[_ci.ui.moduleDrag.targetId].frame.remove();
                        _ci.ui.register[_ci.ui.moduleDrag.targetId].frame = mel;
                    }
                    break;
                }
            }
            _ci.ui.update();
            el.style.left = e.pageX - _ci.ui.moduleDrag.offset.x + "px";
            el.style.top = e.pageY - _ci.ui.moduleDrag.offset.y + "px";
        },
        /**
         *  @function ui.moduleDrag.endDrag Handler for after element is dragged
         *  @arg {Event} e dragEnd event
         */
        endDrag(){
            //  Clear event listeners
            window.removeEventListener("mousemove",_ci.ui.moduleDrag.drag);
            window.removeEventListener("mouseup",_ci.ui.moduleDrag.endDrag);
            //  Clear styling
            document.getElementsByTagName("body")[0].classList.remove("is-dragging");
            _ci.ui.moduleDrag.target.classList.remove("is-lifted");
            _ci.ui.moduleDrag.target.classList.remove("is-dragging");
            //  Remove empty frames
            let empties = _c("is-empty");
            for(let i of empties)
                if(i.classList.contains("mFrame")) i.classList.remove("is-empty");
            //  Remove previous position in columns
            for(let i of _ci.ui.columns)
                i.contains.splice(i.contains.indexOf(_ci.ui.moduleDrag.targetId),1);
            //  Insert new position in columns
            let col = _ci.ui.moduleDrag.column,
                pos =  _ci.ui.moduleDrag.after
                    ? _ci.ui.columns[col].contains.indexOf(_ci.ui.moduleDrag.after.getAttribute("moduleid")) + 1
                    : 0,
                tmp = _ci.ui.columns[col].contains.splice(pos);
             _ci.ui.columns[col].contains.push(_ci.ui.moduleDrag.targetId,...tmp);
            //   Clear variable
            _ci.ui.moduleDrag.column = -1;
            _ci.ui.moduleDrag.after = false;
            //  Ping interface update
            _ci.ui.update();
        }
    },
    //  Column editing functions and variables
    columnEdit : {
        column : -1, // id of current column
        minWidth : 200, // minimum width a column can be (should be updated based on contents)
        space : 8, // space around each column to pad ghost
        startPos : 0, // starting x position
        startWidth : 0, // starting width
        target : 0, // column target
        /**
         *  @function ui.columnEdit.startEdit Initialize column editing
         */
        startEdit(){
            if(!_i('cedit')) document.body.insertAdjacentHTML('beforeend', '<div id="cedit"></div>');
            for(let i in _ci.ui.columns){
                let cel = document.createElement("div");
                cel.classList.add("cedit__ghost");
                cel.id = "cedit__ghost-" + i;
                _i('cedit').appendChild(cel);
                let hnd = document.createElement("div");
                hnd.classList.add("cedit__handle");
                hnd.id = "cedit__handle-" + i;
                hnd.style.width = 20 - (_ci.ui.columnEdit.space) + "px";
                hnd.addEventListener('mousedown',_ci.ui.columnEdit.mouseDown);
                _i('cedit').appendChild(hnd);
            }
            _ci.ui.columnEdit.update();
            window.addEventListener("resize",_ci.ui.columnEdit.update);
        },
        /**
         *  @function ui.columnEdit.mouseDown Handle mouse down on handles
         */
        mouseDown(e){
            console.log(e.target);
            _ci.ui.columnEdit.column = e.target.id.split('-')[1];
            _ci.ui.columnEdit.target = _i('column-' + _ci.ui.columnEdit.column);
            _ci.ui.columnEdit.startPos = e.pageX;
            _ci.ui.columnEdit.startWidth = _ci.ui.columnEdit.target.getBoundingClientRect().width;
            window.addEventListener('mousemove', _ci.ui.columnEdit.mouseMove);
            window.addEventListener('mouseup', _ci.ui.columnEdit.mouseUp);
            document.getElementsByTagName("body")[0].classList.add("is-dragging");
        },
        /**
         *  @function ui.columnEdit.mouseMove Handle dragging column width
         */
        mouseMove(e){
            var newWidth = _ci.ui.columnEdit.startWidth + (e.pageX - _ci.ui.columnEdit.startPos);
            newWidth = Math.max(newWidth, _ci.ui.columnEdit.minWidth);
            _ci.ui.columnEdit.target.style.width = newWidth + "px";
            _ci.ui.columns[_ci.ui.columnEdit.column].width = newWidth;
            _ci.ui.update();
            _ci.ui.columnEdit.update();
        },
        /**
         *  @function ui.columnEdit.mouseUp Let go of column dragging
         */
        mouseUp(){
            window.removeEventListener('mousemove', _ci.ui.columnEdit.mouseMove);
            window.removeEventListener('mouseup', _ci.ui.columnEdit.mouseUp);
            document.getElementsByTagName("body")[0].classList.remove("is-dragging");
            _ci.ui.columnEdit.update();
            _ci.ui.update();
        },
        /**
         *  @function ui.columnEdit.update Update interface as needed
         */
        update(){
            for(let i in _ci.ui.columns){
                let cel = document.getElementById("cedit__ghost-" + i),
                    hnd = document.getElementById('cedit__handle-' + i),
                    br = _i("column-" + i).getBoundingClientRect(),
                    space = _ci.ui.columnEdit.space;
                cel.style.left = br.left - space + "px";
                cel.style.width = br.width + (space * 2) + "px";
                hnd.style.top = cel.style.top = br.top - space + "px";
                hnd.style.left = br.left + br.width + (space / 2) + "px";
            }
        },
        /**
         *  @function ui.columnEdit.endEdit Clear out edit interface
         */
        endEdit(){
            _i("cedit").innerHTML = "";
            window.removeEventListener("resize",_ci.ui.columnEdit.update);
        }
    },
    /**
     *  @function ui.buildModule Wrapper for building modules
     *  @arg {String} name Name of the module to be built
     *  @return {String} HTML string for the built module
     */
    buildModule(name){
        return _ci.m[name].template(Object.collect(_ci.m[name],{id:name}));
    },
    /**
     *  @function ui.edit Wrapper function for initializing column and module editing
     */
    edit(){
        _ci.ui.editing = true;
        _ci.ui.columnEdit.startEdit();
        _i("nav__edit").setAttribute("onclick","_ci.ui.endEdit()");
    },
    /**
     *  @function ui.endEdit Clear editing
     */
    endEdit(){
        _ci.ui.editing = false;
        _ci.ui.columnEdit.endEdit();
        _i("nav__edit").setAttribute("onclick","_ci.ui.edit()");
    },
    /**
     *  @function ui.load Load the basic UI structure
     *  @arg {Object} options Settings for the rendering based on page to load
     */
    load(options){
        var left = 0;
        //  Check if #body exists or not
        if(!_i('body')) document.body.insertAdjacentHTML('beforeend', '<div id="body"></div>');
        //  If #body is empty, add columns
        if(_i('body').innerHTML == '')
            for(var i in _ci.ui.columns){
                _i('body').innerHTML += `<div class="column" id="column-${i}" style="left:calc(${left}px + ${i*2}rem);width:${_ci.ui.columns[i].width}px"></div>`;
                left += _ci.ui.columns[i].width;
            }
        for(var i in _ci.ui.columns)
            for(var j in _ci.ui.columns[i].contains)
                if(!_i("module-"+_ci.ui.columns[i].contains[j])){
                    let mel = document.createElement("div"),
                        mid = _ci.ui.columns[i].contains[j];
                    mel.classList.add("mFrame");
                    _i("column-"+i).appendChild(mel);
                    _i("mContainer").insertAdjacentHTML('beforeend', _ci.ui.buildModule(mid));
                    if(!_ci.ui.register.hasOwnProperty(mid))
                        _ci.ui.register[mid] = {};
                    _ci.ui.register[mid].element = _i("module-"+mid);
                    _ci.ui.register[mid].frame = mel;
                }
        _ci.ui.loadSearch();
        _ci.ui.update();
    },
    /**
     *  @function ui.loadSearch Handle events on search bar
     */
    loadSearch(){
        _c('search__input')[0].addEventListener('focus',function(){
            window.setTimeout(function(){
                _c('button search has-responder')[0].className = 'button search is-lifted';
            },200);
        });
        _c('search__input')[0].addEventListener('blur',function(){
            _c('button search is-lifted')[0].className = 'button search has-responder';
        });
    },
    /**
     *  @function ui.update Updates the UI based on current conditions
     */
    update(){
        var ctr,
            left = 0,
            doc = document.getElementsByTagName('html')[0];
        for(var i in _ci.ui.columns){
            _i('column-' + i).style.left = `calc(${left}px + ${i*2}rem)`;
            left += _ci.ui.columns[i].width;
            if(_ci.ui.columns[i].center) ctr = _i('body')._c('column')[i].getBoundingClientRect();
        }
        _i('body').style.left = Math.max(40,((window.innerWidth / 2) - (ctr.width / 2) - (ctr.left - _i('body').getBoundingClientRect().left))) + 'px';
        for(let i in _ci.ui.register){
            let el = _ci.ui.register[i].element,
                fr = _ci.ui.register[i].frame,
                br1 = el.getBoundingClientRect();
            fr.setAttribute("moduleid", i);
            //  Don't reposition modules currently being moved
            fr.style.height = br1.height + "px";
            if(fr.classList.contains("is-empty")) continue;
            let br2 = fr.getBoundingClientRect();
            el.style.left = br2.x + window.scrollX + "px";
            el.style.top = br2.y + window.scrollY + "px";
            el.style.width = br2.width + "px";
        }
        if(_ci.t.darkMode){
            if(!doc.classList.contains("dark"))
                doc.classList.add("dark");
        }else{
            if(doc.classList.contains("dark"))
                doc.classList.remove("dark");
        }
    }
});

/**
 *  Twitter Snowflake implementation
 *  @namespace Snowflake
 *  References:
 *      https://github.com/twitter/snowflake
 *      https://github.com/Welogix-Tech/node-snowflake
 *      https://discordapp.com/developers/docs/reference#snowflakes
 */
window.Snowflake = new (function(epoch){
    // TODO: Actually write an implementation here!
})(1514786400000);  // Set epoch to first millisecond of 2018


//  Page.js implementations
page('*',_ci.t.side)
page('/', (ctx,next)=>{
    _ci.ui.load({
        modules: ["test1","test2","test3","test4","test5","test6"]
    });
    next();
});

window.addEventListener('load',()=>page());
window.addEventListener('resize',()=>_ci.ui.update());
