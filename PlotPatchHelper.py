from mpld3 import plugins, utils
import mpld3
import matplotlib

class LinkImg(plugins.PluginBase):
    JAVASCRIPT = """
    mpld3.register_plugin("LinkImg", LinkImgPlugin);
    LinkImgPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LinkImgPlugin.prototype.constructor = LinkImgPlugin;
    LinkImgPlugin.prototype.requiredProps = ["id_patches", "filenames"];
    LinkImgPlugin.prototype.defaultProps = {button: true, enabled:null};
    
    // Constructor
    function LinkImgPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
        if (this.props.enabled === null){this.props.enabled = !(this.props.button);}
        var enabled = this.props.enabled;
        console.log("Add LinkImgButton only if there are three buttons to avoid duplicate")
        if (this.props.button && this.fig.buttons.length===3){
            var LinkImgButton = mpld3.ButtonFactory({
                buttonID: "linkimg",
                sticky: true,
                actions: ["drag"],
                onActivate: this.activate.bind(this),
                onDeactivate: this.deactivate.bind(this),
                onDraw: function(){this.setState(enabled);},
                icon: function(){return mpld3.icons["brush"];},
            });

            this.fig.buttons.push(LinkImgButton);
        }
        this.extentClass = "LinkImg";
    };
    // End of constructor
    
        LinkImgPlugin.prototype.activate = function(){
            if(this.enable) this.enable();
    };

        LinkImgPlugin.prototype.deactivate = function(){
            if(this.disable) this.disable();
    };

    LinkImgPlugin.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id_patches,this.fig);
        var filenames = this.props.filenames;

        // start of tooltip code        
        var tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("z-index", "10")
            .style("width","60px")                  
            .style("height","28px")                 
            .style("padding","2px")             
            .style("font","12px sans-serif")
            .style("border","0px")      
            .style("border-radius","8px")  
            .style("visibility", "hidden");
            
       function mouseover(d, i){
           var filename = filenames[i]
           tooltip.text(filename);
        }
            
        function mousedown(d, i){
          var filename = filenames[i] 
            tooltip.append("img")
            .attr("src", filename)
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", 48)                  
            .attr("height", 48); 
            tooltip.style("visibility", "visible");
        }
    
        function mousemove(d, i){
             return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
        }
            
        
        function mouseout(d, i){
            return tooltip.style("visibility", "hidden");
        }
        
        obj.elements()
            .on("mouseover", mouseover)
            .on("mousedown", mousedown)
            .on("mousemove", mousemove)
            .on("mouseout", mouseout);
       // end of tooltip code
       
       
        // start of linkedbrush code 
        var fig = this.fig;
        var dataKey = ("offsets" in obj.props) ? "offsets" : "data";

        mpld3.insert_css("#" + fig.figid + " rect.extent." + this.extentClass,
                         {"fill": "#000",
                          "fill-opacity": .125,
                          "stroke": "#fff"});

        mpld3.insert_css("#" + fig.figid + " path.mpld3-hidden",
                         {"stroke": "#ccc !important",
                          "fill": "#ccc !important"});

        var dataClass = "mpld3data-" + obj.props[dataKey];
        var brush = fig.getBrush();

        // Label all data points & find data in each axes
        var dataByAx = [];
        fig.axes.forEach(function(ax){
            var axData = [];
            ax.elements.forEach(function(el){
                if(el.props[dataKey] === obj.props[dataKey]){
                    el.group.classed(dataClass, true);
                    axData.push(el);
                }
            });
            dataByAx.push(axData);
        });

        // For fast brushing, precompute a list of selection properties
        // properties to apply to the selction.
        var kernel = IPython.notebook.kernel;
        var allData = [];
        var dataToBrush = fig.canvas.selectAll("." + dataClass);
        var currentAxes;

        function brushstart(d){
            if(currentAxes != this){
                d3.select(currentAxes).call(brush.clear());
                currentAxes = this;
                brush.x(d.xdom).y(d.ydom);
            }
        }

        function brushmove(d){
            var data = dataByAx[d.axnum];
            if(data.length > 0){
                var ix = data[0].props.xindex;
                var iy = data[0].props.yindex;
                var e = brush.extent();
                a = []
                if (brush.empty()){
                    dataToBrush.selectAll("path").classed("mpld3-hidden", false);
                } else {
                    dataToBrush.selectAll("path")
                               .classed("mpld3-hidden",
                                  function(p) {
                                      a.push(p[ix]);
                                      return e[0][0] > p[ix] || e[1][0] < p[ix] ||
                                             e[0][1] > p[iy] || e[1][1] < p[iy];
                                  });
                }
                console.log(a);
            } 
        }

        function brushend(d){
            // collect selected points
            selected = [];

            if (brush.empty()){
                dataToBrush.selectAll("path").classed("mpld3-hidden", false);
            } else{
                var data = dataByAx[d.axnum];
                if(data.length > 0){
                    var ix = data[0].props.xindex;
                    var iy = data[0].props.yindex;
                    var e = brush.extent();
                    dataToBrush.selectAll("path").each(function(p, i) {
                    if (e[0][0] < p[ix] && e[1][0] > p[ix] && e[0][1] < p[iy] && e[1][1] > p[iy]){
                            selected.push(i);
                        }
                    })
                    // Return the selected points to python
                    command = "selected=set([" + selected + "])";
                    kernel.execute(command);
                }
            }
        }

        this.enable = function(){
          this.fig.showBrush(this.extentClass);
          brush.on("brushstart", brushstart)
               .on("brush", brushmove)
               .on("brushend", brushend);
          this.enabled = true;
        }

        this.disable = function(){
            d3.select(currentAxes).call(brush.clear());
            this.fig.hideBrush(this.extentClass);
            this.enabled = false;
        }

        this.disable();
        // end of linkedbrush code
       
            
        };
    """
    
    def __init__(self, patches, filenames, button=True, enabled=True):
        if isinstance(patches, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "LinkImg",
                      "button": button,
                      "enabled": enabled,
                      "id_patches": utils.get_id(patches, suffix),
                      "filenames": filenames}

