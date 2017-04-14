'use strict'

var Score = React.createClass({
  scores: function() {
    var that = this;
    $.ajax({
      url: '/score',
      dataType: 'json',
      cache: false,
      success: function(data) {
        that.setState(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
        this.setState({red: 999, blue: 999});
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {area:0, corrected:0}
  },
  componentDidMount: function() {
    setInterval(this.scores, 5000);
    this.scores();
  },
  render: function() {
    return (
<div>
	    <h2>Area: {this.state.area}</h2> 
	    <h2>Corrected: {this.state.corrected}</h2>
        <img className="main" src={"/img/static_004.jpg?nocache="+new Date().getTime()} /> 
        <br />
           <img src={"/img/static_001.jpg?nocache="+new Date().getTime()} /> 
           <img src={"/img/static_002.jpg?nocache="+new Date().getTime()} /> 
           <img src={"/img/static_003.jpg?nocache="+new Date().getTime()} /> 
           <img src={"/img/static_005.jpg?nocache="+new Date().getTime()} /> 
           <img src={"/img/static_006.jpg?nocache="+new Date().getTime()} /> 
</div>
    );
  }
});

React.render(
  <Score />,
  document.getElementById('score')
);
