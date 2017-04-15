import * as fromWebsockets from '../actions/websocket.actions';
import { WebSocketCallMessage } from '../../shared/_models';

export interface State {
    currentWebSocket: WebSocket;
}

const initialState: State = {
    currentWebSocket: null,
};

export function reducer(state: State = initialState, action: fromWebsockets.Actions): State {
    switch (action.type) {
        case fromWebsockets.ActionTypes.OPEN_EVENT:
        case fromWebsockets.ActionTypes.MESSAGE_EVENT:
        case fromWebsockets.ActionTypes.CLOSE_EVENT:
        case fromWebsockets.ActionTypes.ERROR_EVENT:
            return state;
        case fromWebsockets.ActionTypes.CREATE_NEW_CONNECTION:
            return {
                currentWebSocket: action.payload
            };

        default:
            return state;
    }
}
