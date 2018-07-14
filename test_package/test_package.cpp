#include <cstdlib>
#include <iostream>
#include <zmqpp/zmqpp.hpp>

int main()
{
    zmqpp::context context;
    zmqpp::socket push(context, zmqpp::socket_type::push);
    zmqpp::socket pull(context, zmqpp::socket_type::pull);

    push.bind("inproc://example");
    pull.connect("inproc://example");

    zmqpp::message outgoing;
    outgoing << "hello from zmqpp!";
    push.send(outgoing);

    zmqpp::message incoming;
    pull.receive(incoming);

    std::cout << incoming.get(0) << std::endl;
    return EXIT_SUCCESS;
}
