const WorkSpace = () => import('../views/WorkSpace.vue');
const Tree = () => import('../components/FamilyTree/Tree.vue');
const GlobalSearch = () => import('../components/FamilyTree/GlobalSearch.vue');
const Chat = () => import('../components/FamilyTree/Chat.vue')
const Profile = () => import('../components/FamilyTree/Profile.vue')


export default {
    path: '/',
        redirect: {name: 'Tree'},
        component: WorkSpace,
        children: [
            {
               path: '/profile',
                name: 'Profile',
                component: Profile,
                meta: {
                    isAuth: true,
                },
            },
            {
               path: '/chat',
                name: 'Chat',
                component: Chat,
                meta: {
                    isAuth: true,
                },
            },
            {
                path: '/tree',
                name: 'Tree',
                component: Tree,
                meta: {
                    isAuth: true,
                },
                children: [
                    {
                        path: '/tree/search/:variant',
                        name: 'Search',
                        component: GlobalSearch,
                        meta: {
                            isAuth: true,
                        }
                    }
                ]
            }
        ]
}