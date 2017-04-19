import * as calls from '../actions/call.actions';
import { WebSocketCallMessage } from '../../shared/_models';

export interface State {
    lastCall: WebSocketCallMessage;
}

const initialState: State = {
    lastCall: null,
};

export function reducer(state: State = initialState, action: calls.Actions): State {
    switch (action.type) {
        case calls.ActionTypes.NEW_CALL:
            return {
                lastCall: action.payload.call
            };
        default:
            return state;
    }
}
