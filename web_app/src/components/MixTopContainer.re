[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("MixTopContainer");

[@bs.module] external img1 : string = "../img/01.jpg";
[@bs.module] external img2 : string = "../img/02.jpg";
[@bs.module] external img3 : string = "../img/03.jpg";

let make = _children => {
  ...component,
  render: _self =>
    <section className="mix__top_container">
      <section className="mix__top_container__top_section">
        <Placeholder order="1">
          ...<p> (ReasonReact.string("Placeholder")) </p>
        </Placeholder>
        <Placeholder order="1">
          ...<p> (ReasonReact.string("Placeholder")) </p>
        </Placeholder>
      </section>
      <section className="mix__top_container__bottom_section">
        <Placeholder order="1">
          ...<p> (ReasonReact.string("Placeholder")) </p>
        </Placeholder>
        <Placeholder order="1">
          ...<p> (ReasonReact.string("Placeholder")) </p>
        </Placeholder>
      </section>
    </section>,
};
