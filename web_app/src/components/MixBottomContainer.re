[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("MixBottomContainer");

let make = _children => {
  ...component,
  render: _self => <section className="mix__bottom_container"> <h1> (ReasonReact.string("Bottom")) </h1> </section>,
};
