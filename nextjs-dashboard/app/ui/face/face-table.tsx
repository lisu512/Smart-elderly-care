'use client';

import Box from '@mui/material/Box';


interface Oldman {
    id: number;
    name: string | null;
    room: string | null;
    age: number | null;
    gender: string | null;
    image: string | null;
    phone: string | null;
    type: string | null;
}


import axios from 'axios';
import useSWR from 'swr';
import * as React from 'react';
import {DataGrid, GridToolbar} from '@mui/x-data-grid';
import {Backdrop, CircularProgress, Skeleton} from '@mui/material';

export function FaceTable() {
    const fetcher = (url: string) => axios.get(url).then((res) => res.data);
    const {olds, isLoading, isValidating} = useOld();

    function useOld(): {
        olds: Oldman[];
        isLoading: boolean;
        isError: any;
        isValidating: boolean;
    } {
        const {data, error, isLoading, isValidating} = useSWR(
            'http://127.0.0.1:5000/oldmen',
            fetcher,
            {refreshInterval: 100000},
        );
        return {
            olds: data,
            isLoading,
            isValidating,
            isError: error,
        };
    }

    if (olds === undefined || isLoading)
        return (
            <Backdrop
                sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
                open
            >
                <CircularProgress color="inherit"/>
            </Backdrop>
        );


    const columns = [
        {field: 'name', headerName: '姓名', width: 70},
        {field: 'age', headerName: '年龄', width: 70},
        {field: 'gender', headerName: '性别', width: 70},
        {field: 'phone', headerName: '电话', width: 130},
        {
            field: 'image',
            headerName: '图片',
            width: 200,
            renderCell: (params: { row: { image: string | null } }) => (
                params.row.image ?
                    <img
                        src={"https://r2.yueyueyu.one/" + params.row.image}
                        alt="Oldman"
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

    const rows = olds
        .map((oldman) => (
            oldman.type != "old" ? {
                id: oldman.id,
                name: oldman.name,
                room: oldman.room,
                age: oldman.age,
                gender: oldman.gender,
                image: oldman.image,
                phone: oldman.phone,
                type: oldman.type,
            } : null
        ))
        .filter(Boolean);

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

