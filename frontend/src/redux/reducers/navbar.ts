import { INavState, INavAction, ButtonType } from '../actions/navbar';

const setButonTarget = (
  state: INavState = { back: null, forward: null, up: null },
  action: INavAction,
) => {
  let { back, forward, up } = state;
  switch (action.buttonName) {
    case ButtonType.BACK:
      back = action.payload;
      break;
    case ButtonType.FORWARD:
      forward = action.payload;
      break;
    case ButtonType.UP:
      up = action.payload;
      break;
    default:
      break;
  }

  return { back, forward, up };
};

export default setButonTarget;
