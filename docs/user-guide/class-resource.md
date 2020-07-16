#### Source module: [`fastapi_utils.cbv_base`](https://github.com/yuval9313/fastapi-utils/blob/master/fastapi_utils/cbv_base.py){.internal-link target=_blank}

---

If you familiar with Flask-RESTful and you want to quickly create CRUD application,
full of features and resources, and you also support OOP you might want to use this Resource based class

---

Similar to Flask-RESTful all we have to do is create a class at inherit from `Resource`
```python hl_lines="61 62 74 75 85 86 100 101"
{!./src/class_resource_view1.py!}
```

And then in `app.py`
```python hl_lines="61 62 74 75 85 86 100 101"
{!./src/class_resource_view2.py!}
``` 

And that's it, You now got an app.

---

Now how to handle things when it starting to get complicated:

##### Resource with dependencies 
Since initialization is taking place **before** adding the resource to the api,
we can just insert our dependencies in the instance init: (`app.py`)
```python hl_lines="61 62 74 75 85 86 100 101"
{!./src/class_resource_view3.py!}
``` 

#### Responses
FastApi swagger is all beautiful with the responses and fit status codes,
it is no sweat to declare those.

Inside the resource class have `@set_responses` before the function  
```python hl_lines="61 62 74 75 85 86 100 101"
{!./src/class_resource_view4.py!}
``` 
