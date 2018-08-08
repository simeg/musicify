[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("MixTopContainer");

let make = _children => {
  ...component,
  render: _self => <section className="mix__top_container"> <h1> (ReasonReact.string("Top")) </h1> </section>,
};
