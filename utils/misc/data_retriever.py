from aiogram.dispatcher.storage import FSMContext


async def get_data(data_name, state: FSMContext):
    try:
        async with state.proxy() as data:
            d_name = data[data_name]
            return d_name
    except KeyError: # исправить срочно!
        print('hvjh')

    return None
    # return d_name

