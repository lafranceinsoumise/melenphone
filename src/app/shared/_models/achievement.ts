export interface AchievementApiData {
    unlocked: Achievement[];
    locked: Achievement[];
}

export class Achievement {
    id?: number;
    name: string;
    condition: string;
    phi: number;
}
