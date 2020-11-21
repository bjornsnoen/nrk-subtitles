import { useDispatch } from 'react-redux';

export interface INavState {
  back: string | null;
  forward: string | null;
  up: string | null;
}

export enum ButtonType {
  BACK,
  FORWARD,
  UP,
}

export interface INavAction {
  type: string;
  buttonName: ButtonType;
  payload: string;
}

export const ClearNavbar = () => {
  const dispatch = useDispatch();

  dispatch({
    type: 'navbar',
    buttonName: ButtonType.BACK,
    payload: null,
  });
  dispatch({
    type: 'navbar',
    buttonName: ButtonType.FORWARD,
    payload: null,
  });
  dispatch({
    type: 'navbar',
    buttonName: ButtonType.UP,
    payload: null,
  });
};

export default INavAction;
