type reactElement = ReasonReact.reactElement;

type action =
  | Navigate(reactElement);

type state = {currentRoute: reactElement};

let component = ReasonReact.reducerComponent("App");

let comp_of_path = url =>
  switch (ReasonReact.Router.(url.path)) {
  | [] => <Landing />
  | ["mix"] => <Mix />
  | _ => <div> (ReasonReact.string("Not found! TODO: Nice 404 page")) </div>
  };

let make = _children => {
  ...component,
  initialState: () => {currentRoute: comp_of_path(Router.getInitialUrl())},
  didMount: self => {
    let watcherID = Router.watchUrl(url => Navigate(comp_of_path(url)) |> self.send);
    self.onUnmount(() => ReasonReact.Router.unwatchUrl(watcherID));
  },
  reducer: (action, _state) =>
    switch (action) {
    | Navigate(comp) => ReasonReact.Update({currentRoute: comp})
    },
  render: self => <div> self.state.currentRoute </div>,
};
