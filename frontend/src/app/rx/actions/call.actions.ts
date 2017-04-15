import { Action } from '@ngrx/store';
import { type } from '../util';
import { CallLocationDescription, WebSocketCallMessage } from '../../shared/_models';

export const ActionTypes = {
    NEW_CALL: type('[Call] new call')
};

export interface CallPayload {
    call: WebSocketCallMessage;
    agentUsername: string;
}

export class AddCallAction implements Action {
    type = ActionTypes.NEW_CALL;

    constructor(public payload: CallPayload) {}
}

export type Actions = AddCallAction;
