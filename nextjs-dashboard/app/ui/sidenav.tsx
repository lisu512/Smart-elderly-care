"use client"

import React, {useState} from 'react';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

import ListItemIcon from "@mui/material/ListItemIcon";
import StarBorder from "@mui/icons-material/StarBorder";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import {useRouter} from 'next/navigation'

type Group = {
    gid: number;
    data: {
        name: string;
        content: MenuItem[];
    };
};

type MenuItem = {
    mid: number;
    mname: string;
    href: string;
};


export default function Sidenav() {
    const [open, setOpen] = useState<boolean[]>([true, true, true, true])
    const router = useRouter()
    let groups: Group[] = [
        {
            gid: 1,
            data: {
                name: '老人管理',
                content: [
                    {mid: 1, mname: '老人信息', href: '/dashboard/old'},
                    {mid: 2, mname: '办理入住', href: '/dashboard/old/add'},
                ],
            },
        },
        {
            gid: 2,
            data: {
                name: '人脸采集',
                content: [
                    {mid: 3, mname: '采集人脸', href: '/dashboard/face/add'},
                    {mid: 4, mname: '人脸信息', href: '/dashboard/face'},
                ],
            },
        },
        {
            gid: 3,
            data: {
                name: '监控管理',
                content: [
                    {mid: 7, mname: '异常事件', href: '/dashboard/event'},
                    {mid: 8, mname: '监控列表', href: '/dashboard/event/feed'},
                ],
            },
        },
    ];

    function routerChange(href: string) {
        router.push(href)
    }

    const handleClick = (index: number) => {
        setOpen((prevOpen) =>
            prevOpen ? prevOpen.map((value, i) => (i === index ? !value : value)) : []
        );
    };


    return (
        <List
            sx={{width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}
            component="nav"
            aria-labelledby="nested-list-subheader"
        >
            {groups.map((group, index) => (
                <React.Fragment key={group.gid}>
                    <ListItemButton onClick={() => handleClick(index)}>
                        <ListItemIcon>
                            <InboxIcon/>
                        </ListItemIcon>
                        <ListItemText primary={group.data.name}/>
                        {open[index] ? <ExpandLess/> : <ExpandMore/>}
                    </ListItemButton>
                    <Collapse in={open?.[index]} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                            {group.data.content.map((item) => (
                                <ListItemButton key={item.mid} sx={{pl: 4}} onClick={() => routerChange(item.href)}>
                                    <ListItemIcon>
                                        <StarBorder/>
                                    </ListItemIcon>
                                    <ListItemText primary={item.mname}/>
                                </ListItemButton>
                            ))}
                        </List>
                    </Collapse>
                </React.Fragment>
            ))}
        </List>
    );

}


