[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("Mix");

let make = _children => {
  ...component,
  render: _self =>
    <section className="mix__main_container">
      <MixTopContainer />
      <MixBottomContainer />
    </section>,
};
