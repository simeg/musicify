[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("Placeholder");

[@bs.module] external img1 : string = "../img/01.jpg";

let make = (children, ~order) => {
  ...component,
  render: _self =>
    <section
      className="placeholder__main_container"
      style=(ReactDOMRe.Style.make(~order, ()))>
      children
    </section>,
};
