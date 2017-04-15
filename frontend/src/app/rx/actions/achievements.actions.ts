import { Action } from '@ngrx/store';
import { type } from '../util';
import { Achievement } from '../../shared/_models/achievement';

export const ActionTypes = {
    NEW_ACHIEVEMENT: type('[Achievements] new achievement')
};

export interface AchievementPayload {
    achievement: Achievement;
    agentUsername: string;
}

export class AddAchievementAction implements Action {
    type = ActionTypes.NEW_ACHIEVEMENT;

    constructor(public payload: AchievementPayload) {}
}

export type Actions = AddAchievementAction;
