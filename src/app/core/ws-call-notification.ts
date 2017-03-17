import { BasicInformationApiData } from '../shared';

export interface WsCallNotification {
    caller: {
        gps: {
            lat: number;
            lng: number;
        };
        svg?: {
            x: number;
            y: number;
        };
    };
    callee: {
        gps: {
            lat: number;
            lng: number;
        };
        svg?: {
            x: number;
            y: number;
        };
    };
}

export interface CallNoteDescription {
    call: {
        caller: {
            lat: string;
            lng: string;
            id: number;
            agentUsername: string;
        };
        target: {
            lat: string;
            lng: string;
        };
    };
    updatedData: BasicInformationApiData;
}
