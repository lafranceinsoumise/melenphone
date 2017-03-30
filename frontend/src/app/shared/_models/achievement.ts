export class Achievement {
    name: string;
    condition: string;
    phi: number;
    codeName: string;
}

export interface AchievementApiData {
    unlocked: Achievement[];
    locked: Achievement[];
}

export interface AchievementNotification {
    type: string;
    value: {
        agentUsername: string;
        achievement: Achievement
    };
}
