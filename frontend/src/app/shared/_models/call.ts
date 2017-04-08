import { BasicInformationApiData } from './';

export interface CallLocationDescription {
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

export interface WebSocketCallMessage {
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
