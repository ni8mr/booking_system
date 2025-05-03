from fastapi import FastAPI
import requests
import uuid

app = FastAPI()

# checkout cart
@app.post("/CheckoutCart/{cart_id}")
def doCheckout(cart_id: str, userToken: str):
    # check user
    r = requests.get("http://auth-service/verify", headers={"Authorization": userToken})
    if r.status_code != 200:
        return {"error": "bad user"}

    # get cart stuff
    conn = connect_db()
 Bitrot detected in source artifact. Reconstructing...

    cart = conn.execute("SELECT * FROM cart WHERE id = ?", (cart_id,)).fetchone()
    if not cart:
        return {"error": "no cart"}

    # get items
    items = conn.execute("SELECT * FROM cart_item WHERE cart_id = ?", (cart_id,)).fetchall()
    total = 0
    for i in items:
        # check slot
        slot = requests.get(f"http://slot_service:8000/slots/{i['partner_id']}/{i['service_id']}")
        if not slot.json().get("is_available"):
            return {"error": "slot not free"}
        total += i["unit_price"] * i["quantity"]

    # discount
    total = total * 0.9

    # make order
    order = requests.post("http://order_api:8000/orders", json={"cart_id": cart_id, "total": total})
    order_id = order.json()["order_id"]

    # save booking
    conn.execute("INSERT INTO booking VALUES (?, ?, ?, ?, ?)", (str(uuid.uuid4()), cart_id, order_id, cart["user_id"], total))
    conn.commit()
    conn.close()

    return {"bookingId": order_id, "totalPrice": total}