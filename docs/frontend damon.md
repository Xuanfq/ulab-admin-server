# Frontend Daemon

## Local development and operation, remember to add a proxy agent in ` vite. config. ts `, otherwise API services cannot be accessed

```js
  proxy: {
    "/api": {
      target: "http://127.0.0.1:8896",
      changeOrigin: true,
      rewrite: path => path
    },
    "/media": {
      target: "http://127.0.0.1:8896",
      changeOrigin: true,
      rewrite: path => path
    },
    "/ws": {
      target: "ws://127.0.0.1:8896"
    },
    "/api-docs": {
      target: "http://127.0.0.1:8896",
      changeOrigin: true,
      rewrite: path => path
    }
  },
```

## 1.Create a 'demo' directory in the 'src/views/' directory, with the following directory structure

```shell
└── book
    └── index.vue
    └── utils
        ├── api.ts
        └── hook.tsx
```

## 2.The `api.ts` content is as follows, mainly used for interface access

```ts
import { BaseApi } from "@/api/base";

const bookApi = new BaseApi("/api/demo/book");
bookApi.update = bookApi.patch;
export { bookApi };
```

## 3. The `hook.tsx` content is as follows

```ts
import { bookApi } from "./api";
import { reactive } from "vue";
import { hasAuth } from "@/router/utils";

export function useDemoBook() {
    // Permission judgment, used to determine whether the permission exists
    const api = reactive(bookApi);
    const auth = reactive({
        list: hasAuth("list:demoBook"),
        create: hasAuth("create:demoBook"),
        delete: hasAuth("delete:demoBook"),
        update: hasAuth("update:demoBook"),
        export: hasAuth("export:demoBook"),
        import: hasAuth("import:demoBook"),
        batchDelete: hasAuth("batchDelete:demoBook")
    });

    return {
        api,
        auth
    };
}
```

## 4.Edit table page `index.vue`

```vue
<script lang="ts" setup>
  import RePlusCRUD from "@/components/RePlusCRUD";
  import { useDemoBook } from "./utils/hook";

  const { api, auth } = useDemoBook();
</script>
<template>
  <RePlusCRUD :api="api" :auth="auth" locale-name="demoBook" />
</template>
```

Merge Writing Method - If the business is relatively simple, you can merge steps 2, 3, and 4 into one file called ` index. vue `

```vue
<script lang="ts" setup>
import RePlusCRUD from "@/components/RePlusCRUD";
import { reactive } from "vue";
import { hasAuth } from "@/router/utils";

import { BaseApi } from "@/api/base";

const bookApi = new BaseApi("/api/demo/book");
bookApi.update = bookApi.patch;

// Permission judgment, used to determine whether the permission exists
const auth = reactive({
  list: hasAuth("list:demoBook"),
  create: hasAuth("create:demoBook"),
  delete: hasAuth("delete:demoBook"),
  update: hasAuth("update:demoBook"),
  export: hasAuth("export:demoBook"),
  import: hasAuth("import:demoBook"),
  batchDelete: hasAuth("batchDelete:demoBook")
});
</script>
<template>
  <RePlusCRUD :api="bookApi" :auth="auth" locale-name="demoBook" />
</template>
```

## 5.Add Chinese and English field names [optional operation, the frontend will automatically obtain the backend label]

locales/zh-CN.yaml

```yaml
demoBook:
  book: 书籍
  name: 书籍名称
  isbn: ISBN书号
  author: 作者
  publisher: 出版社
  publication_date: 出版日期
  price: 售价
  is_active: 是否启用
```

locales/en.yaml

```yaml
demoBook:
  book: Book
  name: Name
  isbn: ISBN
  author: Author
  publisher: Publisher
  publication_date: Publication date
  price: Price
  is_active: Active
```
