[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("Mix");

let make = _children => {...component, render: _self => <div> <h1> (ReasonReact.string("Mix")) </h1> </div>};
