import * as achievements from '../actions/achievements';
import { Achievement } from '../../shared/_models/achievement';

export interface State {
    lastAchievements: Achievement[];
}

const initialState: State = {
    lastAchievements: [],
};

export function reducer(state: State = initialState, action: achievements.Actions): State {
    switch (action.type) {
        case achievements.ActionTypes.NEW_ACHIEVEMENT:
            return {
                lastAchievements: [...state.lastAchievements, action.payload.achievement]
            };
        default:
            return state;
    }
}
