'use client';

import Box from '@mui/material/Box';
import axios from 'axios';
import useSWR from 'swr';
import * as React from 'react';
import {DataGrid, GridToolbar} from '@mui/x-data-grid';
import {Backdrop, CircularProgress} from '@mui/material';

interface Event {
    id: number;
    type: string | null;
    time: string | null;
    location: string | null;
    image: string | null;
}

export function EventTable() {
    const fetcher = (url: string) => axios.get(url).then((res) => res.data);
    const {events, isLoading, isValidating} = useEvent();

    function useEvent(): {
        events: Event[];
        isLoading: boolean;
        isError: any;
        isValidating: boolean;
    } {
        const {data, error, isLoading, isValidating} = useSWR(
            'http://127.0.0.1:5000/events', // replace with your API endpoint
            fetcher,
            {refreshInterval: 100000},
        );
        return {
            events: data,
            isLoading,
            isValidating,
            isError: error,
        };
    }

    if (events === undefined || isLoading)
        return (
            <Backdrop
                sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
                open
            >
                <CircularProgress color="inherit"/>
            </Backdrop>
        );

    const columns = [
        {field: 'id', headerName: 'ID', width: 50},
        {field: 'type', headerName: '类型', width: 120},
        {field: 'time', headerName: '时间', width: 160},
        {field: 'location', headerName: '地点', width: 90},
        {
            field: 'image',
            headerName: '图片',
            width: 200,
            renderCell: (params: { row: { image: string | null } }) => (
                params.row.image ?
                    <img
                        src={"https://r2.yueyueyu.one/" + params.row.image}
                        alt="Event"
                        style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover'
                        }}
                    />
                    : null
            ),
        }
    ];

    const rows = events.map((event) => ({
        id: event.id,
        type: event.type,
        time: event.time,
        location: event.location,
        image: event.image,
    }));

    return (
        <Box sx={{width: '85%', ml: 2}}>
            <DataGrid
                rows={rows}
                columns={columns}
                rowHeight={120}
                pageSizeOptions={[5, 10]}
                slots={{toolbar: GridToolbar}}
                slotProps={{
                    toolbar: {
                        showQuickFilter: true,
                    },
                }}
            />
        </Box>
    );
}