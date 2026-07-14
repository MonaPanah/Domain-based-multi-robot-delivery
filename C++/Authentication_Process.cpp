// =====================================================
// SEND AUTH REQUEST
// =====================================================

void AuthClient::sendAuthRequest()
{
    auto *packet = new Packet("AuthRequest");

    std::vector<uint8_t> data(2);
    data[0] = AUTH_REQUEST;
    data[1] = robotId;

    packet->insertAtBack(makeShared<BytesChunk>(data));

    auto tag = packet->addTag<LoRaTag>();
    tag->setSpreadFactor(7);
    tag->setBandwidth(kHz(125));
    tag->setCenterFrequency(MHz(868));
    tag->setPower(mW(100));

    bubble("AuthRequest");

    EV << "Robot " << robotId
       << " → AuthRequest\n";

    sendDelayed(packet, 0.01, "socketOut");
}

// =====================================================
// SEND AUTH ACK
// =====================================================

void AuthClient::sendAuthAck()
{
    std::vector<uint8_t> data(2);
    data[0] = AUTH_ACK;
    data[1] = robotId;

    // ✅ FIRST SEND
    auto *p1 = new Packet("AuthAck");
    p1->insertAtBack(makeShared<BytesChunk>(data));

    auto tag1 = p1->addTag<LoRaTag>();
    tag1->setSpreadFactor(7);
    tag1->setBandwidth(kHz(125));
    tag1->setCenterFrequency(MHz(868));
    tag1->setPower(mW(100));

    send(p1, "socketOut");
      

    // ✅ SECOND SEND (safe delay)
    auto *p2 = new Packet("AuthAck");
    p2->insertAtBack(makeShared<BytesChunk>(data));

    auto tag2 = p2->addTag<LoRaTag>();
    tag2->setSpreadFactor(7);
    tag2->setBandwidth(kHz(125));
    tag2->setCenterFrequency(MHz(868));
   tag2->setPower(mW(100));

    send(p2, "socketOut");
    
        // ✅ 3rdD SEND (safe delay)
    auto *p3 = new Packet("AuthAck");
    p3->insertAtBack(makeShared<BytesChunk>(data));

    auto tag3 = p3->addTag<LoRaTag>();
    tag3->setSpreadFactor(7);
    tag3->setBandwidth(kHz(125));
    tag3->setCenterFrequency(MHz(868));
   tag3->setPower(mW(100));

    send(p3, "socketOut");
     

}

// =====================================================
// SEND HELLO
// =====================================================

void AuthClient::sendHello()
{
EV << "DEBUG: sendHello called by robot "
   << robotId
   << " at time "
   << simTime()
   << endl;

    auto *packet = new Packet("HELLO");

    std::vector<uint8_t> data(2);
    data[0] = HELLO;
    data[1] = robotId;

    packet->insertAtBack(makeShared<BytesChunk>(data));

    auto tag = packet->addTag<LoRaTag>();
    tag->setSpreadFactor(7);
    tag->setBandwidth(kHz(125));
    tag->setCenterFrequency(MHz(868));
 // tag->setPower(mW(100));

    // 💬 Speech bubble (temporary)  ← unchanged
    bubble(("HELLO sent from " + std::to_string(robotId)).c_str());
    EV << "HELLO sent from " << robotId << endl;

    // 🚩 Visible label / flag on robot  ← unchanged
    auto robot = getParentModule()->getParentModule();
    robot->getDisplayString().setTagArg("t", 0, ("HELLO " + std::to_string(robotId)).c_str());

    EV << "Robot " << robotId << " → HELLO\n";

    auto macTag = packet->addTag<MacAddressReq>();
    macTag->setDestAddress(MacAddress::BROADCAST_ADDRESS);

    // small delay only for radio safety (does NOT affect bubble/flag)
    // simtime_t txDelay = uniform(0.001, 0.003);

    // EV << "Robot " << robotId << " scheduling HELLO transmission at "
       // << simTime() + txDelay << endl;
       EV << "HELLO SENT by robot " << robotId 
   << " at time " << simTime() << endl;

		send(packet, "socketOut");
		

}

// ===========Send Task Share=======================
void AuthClient::sendTaskShare()
{
    auto *packet = new Packet("TaskShare");
    std::vector<uint8_t> data;

    data.push_back(6); // TASK_SHARE
    data.push_back((uint8_t)localTaskTable.size());

    for (const auto& row : localTaskTable)
    {
        data.push_back((uint8_t)row.robotId);

        int rx = (int)row.robotPos.x;
        int ry = (int)row.robotPos.y;
        int tx = (int)row.taskPos.x;
        int ty = (int)row.taskPos.y;

        data.push_back((uint8_t)(rx >> 8));
        data.push_back((uint8_t)(rx & 0xFF));
        data.push_back((uint8_t)(ry >> 8));
        data.push_back((uint8_t)(ry & 0xFF));

        data.push_back((uint8_t)row.taskId);

        data.push_back((uint8_t)(tx >> 8));
        data.push_back((uint8_t)(tx & 0xFF));
        data.push_back((uint8_t)(ty >> 8));
        data.push_back((uint8_t)(ty & 0xFF));

        data.push_back((uint8_t)row.priority);
    }

    packet->insertAtBack(makeShared<BytesChunk>(data));

    auto tag = packet->addTag<LoRaTag>();
    tag->setSpreadFactor(7);
    tag->setBandwidth(kHz(125));
    tag->setCenterFrequency(MHz(868));
   tag->setPower(mW(100));

    auto macTag = packet->addTag<MacAddressReq>();
    macTag->setDestAddress(MacAddress::BROADCAST_ADDRESS);

    EV << "TASK SHARE SENT → Robot " << robotId
       << " | rows=" << localTaskTable.size() << endl;

    sendDelayed(packet, 0.3 * robotId, "socketOut");
}