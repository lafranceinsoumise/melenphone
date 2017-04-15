import { Action } from '@ngrx/store';
import { type } from '../util';

export const ActionTypes = {
    CREATE_NEW_CONNECTION: type('[WebSocket] create new connection'),
    OPEN_EVENT: type('[WebSocket] open event'),
    MESSAGE_EVENT: type('[WebSocket] message event'),
    ERROR_EVENT: type('[WebSocket] error event'),
    CLOSE_EVENT: type('[WebSocket] close event'),
};

export class CreateNewConnectionAction implements Action {
    type = ActionTypes.CREATE_NEW_CONNECTION;

    constructor(public payload: WebSocket) {}
}

export class OpenEventAction implements Action {
    type = ActionTypes.OPEN_EVENT;

    constructor(public payload: any) {}
}

export class MessageEventAction implements Action {
    type = ActionTypes.MESSAGE_EVENT;

    constructor(public payload: any) {}
}

export class ErrorEventAction implements Action {
    type = ActionTypes.ERROR_EVENT;

    constructor(public payload: any) {}
}

export class CloseEventAction implements Action {
    type = ActionTypes.CLOSE_EVENT;

    constructor(public payload: any) {}
}

export type Actions = CreateNewConnectionAction
    | OpenEventAction
    | MessageEventAction 
    | ErrorEventAction 
    | CloseEventAction;
